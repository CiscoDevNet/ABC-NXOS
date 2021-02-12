*** Settings ***
Documentation      Robot Framework test script
Library            SSHLibrary

*** Variables ***
${host}             10.10.20.177
${username}         cisco
${password}         cisco
${alias}            dist-sw01#


*** Test Cases ***
Test SSH Connection
    Open Connection    ${host}        alias=${alias}
    Login              ${username}    ${password}    delay=1
Modify Terminal    
    Write  terminal length 0

Verify version
    ${output}=         Execute Command    show version
    Should Contain    ${output}           version 9.2(3)
Verify Ospf  
    ${output}=         Execute Command    show run interface Ethernet1/3
    Should Contain    ${output}          ip router ospf 1 area 0.0.0.0

Verify 5 up interfaces
    ${output}=         Execute Command    show interface brief 
    Should Contain    ${output}          up    5



