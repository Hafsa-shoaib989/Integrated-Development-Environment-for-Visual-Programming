const { ipcRenderer } = require('electron');
const fs = require('fs');
const path = require('path');

let workspace;  // define workspace at the top for proper scope

document.addEventListener('DOMContentLoaded', () => {
    console.log('Blockly workspace is being initialized...');
    const blocklyDiv = document.getElementById('blocklyDiv');
    workspace = Blockly.inject(blocklyDiv, {
        toolbox: {
            "kind": "categoryToolbox",
            "contents": [
                {
                    "kind": "category",
                    "name": "Logic",
                    "contents": [
                        {
                            "kind": "block",
                            "type": "controls_if"
                        },
                        {
                            "kind": "block",
                            "type": "logic_compare"
                        }
                    ]
                },
                {
                    "kind": "category",
                    "name": "Loops",
                    "contents": [
                        {
                            "kind": "block",
                            "type": "controls_repeat_ext"
                        }
                    ]
                },
                {
                    "kind": "category",
                    "name": "Math",
                    "contents": [
                        {
                            "kind": "block",
                            "type": "math_number"
                        },
                        {
                            "kind": "block",
                            "type": "math_arithmetic"
                        }
                    ]
                },
                {
                    "kind": "category",
                    "name": "Database",
                    "contents": [
                        {
                            "kind": "block",
                            "type": "fetch_from_database"
                        }
                    ]
                }
            ]
        }
    });
    console.log('Blockly workspace initialized.');

    //compile button
    document.getElementById('compile').addEventListener('click', () => {
        try {
            const xml = Blockly.Xml.workspaceToDom(workspace);
            const xml_text = Blockly.Xml.domToPrettyText(xml);  // domToPrettyText for better format
            const csvFilePath = path.join(__dirname, 'csv_output', 'blockly_output.csv');
            
            fs.writeFileSync(csvFilePath, xml_text);
            alert('CSV file generated successfully.');
        } catch (error) {
            alert('Failed to generate CSV file: ' + error.message);
        }
    });
    
    //run button
    document.getElementById('run').addEventListener('click', () => {
        ipcRenderer.send('run-script');  // Send IPC message to main process
    });
});

//block status
ipcRenderer.on('update-block-status', (event, message) => {
    try {
        console.log('Updating block status with message:', message);
        const decodedMessage = new TextDecoder("utf-8").decode(message);
        const statuses = JSON.parse(decodedMessage);
        Object.keys(statuses).forEach(blockId => {
            console.log('Checking block ID:', blockId);
            const block = workspace.getBlockById(blockId);  // Use properly scoped workspace
            if (block) {
                const color = statuses[blockId] === 'success' ? '#00FF00' : '#FF0000';
                console.log(`Updating block color for ${blockId} to ${color}`);
                block.setColour(color);
                block.render();  
            } else {
                console.error(`Block with ID ${blockId} not found`);
            }
        });
    } catch (error) {
        console.error('Error updating block statuses:', error);
    }
});
