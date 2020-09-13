# arbitrary-yang

These files are examples generated from an arbitrary YANG model describing a sportsball team and a roster of players.  While the YANG generates a model, for illustrative purposes, this provides only one half of the required information when performing service development against NSO.  In order to easily generate a template structure from arbitrary YANG, we can use `pyang` with different outformats.

# Usage

sportsball.yang hosts the sample data model given in the Powerpoint.  From this model -- we can explore the functionality of `pyang` (included with the NSO installation)

## XML Output

By invoking `pyang` using the following, we can natively explore the XML result from the data model

`pyang -f sample-xml-skeleton sportsball.yang`

This output will not be "pretty" formatted, but you can add newlines as appropriate.  Alternatively -- by adding `-o <filename>.<extension>`, you can output the file to be saved rather than reviewing through stdin.

## YIN

If we have YANG, we must have the YIN, yes?
YIN is an "XML-like" formatted output of the data model.  Unlike the XML output above, this is not for a response to the model (as would be done in a service template for NSO), but is simply a different way to visualize the model.

`pyang -f yin sportsball.yang`

## Tree

Tree format is often used to clearly and quickly visualize the hierarchy of YANG models.  Often a single model will have one or mode modules, each with one or more submodules, making it difficult to follow using YIN or XML.  Tree provides a concise view of the modules, leafs, and required data types for each leaf.

`pyang -f tree sportsball.yang`
