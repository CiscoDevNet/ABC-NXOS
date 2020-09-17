import os
import sys
import yaml
import argparse
import logging
import logging.handlers as handlers
import os
import argparse
import json
import glob
import subprocess

class CustomFormatter(logging.Formatter):
    def __init__(self, patterns=[], fmt=None, datefmt=None, style='%'):
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)
        self.patterns = patterns

    def format(self, record: logging.LogRecord):
        res = super(CustomFormatter, self).format(record)
        for pattern in self.patterns:
            res = res.replace(pattern, "*******")
        return res

def default(name, level="INFO", patterns=[], logfile=None):
    ch = logging.StreamHandler()
    custom_formatter = CustomFormatter(patterns=patterns, fmt="[%(asctime)s] [%(levelname)8s] (%(filename)s:%(lineno)s) --- %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    ch.setLevel(level)
    logger = logging.getLogger(name)
    logger.handlers = []
    ch.setFormatter(custom_formatter)
    logger.addHandler(ch)
    logger.setLevel(logging.DEBUG)
    if not logfile == None:
        # 100 MB Log Files
        rfh = handlers.RotatingFileHandler(logfile, mode='a+',maxBytes=104857600, backupCount=2)
        rfh.setLevel(logging.DEBUG)
        rfh.setFormatter(custom_formatter)
        logger.addHandler(rfh)
    return logger

def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line 
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

def create_inventory_file(filepath, ip):
    with open(filepath, 'w') as f:
        contents = (
            f"[nxos]"
            f"\n"
            f"{ip}"
        )
        f.write(contents)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='cicd-automation')
    parser.add_argument('--log', default="DEBUG")
    parser.add_argument('--config_dir', default="config")
    parser.add_argument('--actions_dir', default="actions")
    parser.add_argument('--env_file', default="env.yml")
    parser.add_argument('--inventory_file', default="inventory")
    parser.add_argument('--path', default='./')
    args = parser.parse_args()
    logger = default("cicd-basics", level=args.log)

    path = os.path.abspath(args.path)
    env_file = os.path.abspath(args.env_file)
    inventory_file = os.path.abspath(args.inventory_file)
    
    for filename in glob.iglob(path + f'/{args.config_dir}/**', recursive=True):
        logger.debug("processing file/folder %s", filename)
        config_info = dict()
        environments = []
        if not os.path.isdir(filename):
            logger.debug("processing file " + filename)
            with open(filename) as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
                for item in data["items"]:
                    env_data = dict()
                    for key in item.keys():
                        env_data.setdefault(f'nxos_{key}', item[key])
                    environments.append(env_data)
                config_info["ip"] = data["ip"]
                action = data["action"]
                logger.debug("environments action=%s json=%s", action, environments)
                if action not in config_info:
                    config_info[action] = environments
                else:
                    config_info[action] = config_info[action] + environments

            # run this for each config_info                    
            with open(env_file, 'w') as f:
                logger.debug("writing env_file=%s", env_file)
                f.write(yaml.dump(config_info))
            for actionfile in glob.iglob(path + f'/{args.actions_dir}/**', recursive=True):
                if os.path.isfile(actionfile):
                    normalize_action_name = os.path.basename(actionfile).replace(".yml", "").replace("-", "_")
                    if normalize_action_name in config_info:
                        logger.debug("processing action=%s file=%s", normalize_action_name, actionfile)
                        create_inventory_file(inventory_file, config_info["ip"])
                        cmd = ['ansible-playbook', '-i', f'{inventory_file}', f'{actionfile}', "--extra-vars", f'@{env_file}']
                        logger.debug("running cmd='%s'", ' '.join(cmd))
                        for cmd_line_result in execute(cmd):
                            print(cmd_line_result, end="")
                    else:
                        logger.debug("skipping action=%s file=%s", normalize_action_name, actionfile)
