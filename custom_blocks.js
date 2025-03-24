Blockly.defineBlocksWithJsonArray([
    {
        "type": "fetch_from_database",
        "message0": "fetch from database %1",
        "args0": [
            {
                "type": "input_value",
                "name": "QUERY"
            }
        ],
        "previousStatement": null,
        "nextStatement": null,
        "colour": 230,
        "tooltip": "",
        "helpUrl": ""
    },
    {
        "type": "controls_if",
        "message0": "if %1 then %2 else %3",
        "args0": [
            {
                "type": "input_value",
                "name": "IF0"
            },
            {
                "type": "input_statement",
                "name": "DO0"
            },
            {
                "type": "input_statement",
                "name": "ELSE"
            }
        ],
        "previousStatement": null,
        "nextStatement": null,
        "colour": 210,
        "tooltip": "",
        "helpUrl": ""
    },
    {
        "type": "controls_repeat_ext",
        "message0": "repeat %1 times %2 else %3",
        "args0": [
            {
                "type": "input_value",
                "name": "TIMES"
            },
            {
                "type": "input_statement",
                "name": "DO"
            },
            {
                "type": "input_statement",
                "name": "ELSE"
            }
        ],
        "previousStatement": null,
        "nextStatement": null,
        "colour": 120,
        "tooltip": "",
        "helpUrl": ""
    }
]);

Blockly.JavaScript['fetch_from_database'] = function(block) {
    var query = Blockly.JavaScript.valueToCode(block, 'QUERY', Blockly.JavaScript.ORDER_ATOMIC);
    var code = `fetchFromDatabase(${query});\n`;
    return code;
};

Blockly.JavaScript['controls_if'] = function(block) {
    var condition = Blockly.JavaScript.valueToCode(block, 'IF0', Blockly.JavaScript.ORDER_ATOMIC);
    var branch = Blockly.JavaScript.statementToCode(block, 'DO0');
    var elseBranch = Blockly.JavaScript.statementToCode(block, 'ELSE');
    var code = `if (${condition}) {\n${branch}} else {\n${elseBranch}}\n`;
    return code;
};

Blockly.JavaScript['controls_repeat_ext'] = function(block) {
    var repeats = Blockly.JavaScript.valueToCode(block, 'TIMES', Blockly.JavaScript.ORDER_ATOMIC);
    var branch = Blockly.JavaScript.statementToCode(block, 'DO');
    var elseBranch = Blockly.JavaScript.statementToCode(block, 'ELSE');
    var code = `for (var count = 0; count < ${repeats}; count++) {\n${branch}} else {\n${elseBranch}}\n`;
    return code;
};
