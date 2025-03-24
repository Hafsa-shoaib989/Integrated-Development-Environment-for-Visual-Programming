import os
import xml.etree.ElementTree as ET
import tkinter as tk
import mysql.connector
import asyncio
import websockets
import json

def fetch_from_database(query):
    print(f"Executing database query: {query}")
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Doradoradora1;',
        database='test_database'
    )
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    print(f"Database query result: {results}")
    return results

async def notify_statuses(statuses):
    uri = "ws://localhost:8000"
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps(statuses))

def execute_block(block, variables, output, statuses):
    ns = {'b': 'https://developers.google.com/blockly/xml'}
    block_type = block.get('type')
    print(f"Executing block: {block_type}")
    status = 'success'
    try:
        if block_type == 'controls_if':
            condition_block = block.find('b:value[@name="IF0"]/b:block', ns)
            else_block = block.find('b:statement[@name="ELSE"]/b:block', ns)
            if condition_block is not None:
                if_condition = execute_block(condition_block, variables, output, statuses)
                output.append(f'If condition executed: {if_condition}')
                print(f'If condition executed: {if_condition}')
                if if_condition:
                    do_block = block.find('b:statement[@name="DO0"]/b:block', ns)
                    while do_block is not None:
                        execute_block(do_block, variables, output, statuses)
                        do_block = do_block.find('b:next/b:block', ns)
                elif else_block is not None:
                    while else_block is not None:
                        execute_block(else_block, variables, output, statuses)
                        else_block = else_block.find('b:next/b:block', ns)
            else:
                output.append('If condition block not found')
                print('If condition block not found')
                raise ValueError('If condition block not found')
        elif block_type == 'controls_repeat_ext':
            times_block = block.find('b:value[@name="TIMES"]/b:block', ns)
            if times_block is not None:
                repeat_times = int(execute_block(times_block, variables, output, statuses))
                output.append(f'Repeat {repeat_times} times')
                print(f'Repeat {repeat_times} times')
                for _ in range(repeat_times):
                    statement_block = block.find('b:statement[@name="DO"]/b:block', ns)
                    while statement_block is not None:
                        execute_block(statement_block, variables, output, statuses)
                        statement_block = statement_block.find('b:next/b:block', ns)
                    else_block = block.find('b:statement[@name="ELSE"]/b:block', ns)
                    if else_block is not None:
                        while else_block is not None:
                            execute_block(else_block, variables, output, statuses)
                            else_block = else_block.find('b:next/b:block', ns)
            else:
                output.append('Repeat times block not found')
                print('Repeat times block not found')
                raise ValueError('Repeat times block not found')
        elif block_type == 'math_number':
            field = block.find('b:field[@name="NUM"]', ns)
            if field is not None:
                num = field.text
                output.append(f'Number: {num}')
                print(f"Number: {num}")
                return int(num)
            else:
                output.append('Number field not found')
                print('Number field not found')
                raise ValueError('Number field not found')
        elif block_type == 'logic_compare':
            operator_field = block.find('b:field[@name="OP"]', ns)
            if operator_field is not None:
                operator = operator_field.text
                left_block = block.find('b:value[@name="A"]/b:block', ns)
                right_block = block.find('b:value[@name="B"]/b:block', ns)
                if left_block is not None and right_block is not None:
                    left_value = execute_block(left_block, variables, output, statuses)
                    right_value = execute_block(right_block, variables, output, statuses)
                    if operator == 'EQ':
                        result = left_value == right_value
                    elif operator == 'NEQ':
                        result = left_value != right_value
                    elif operator == 'LT':
                        result = left_value < right_value
                    elif operator == 'LTE':
                        result = left_value <= right_value
                    elif operator == 'GT':
                        result = left_value > right_value
                    elif operator == 'GTE':
                        result = left_value >= right_value
                    output.append(f'Logic compare operation ({operator}): {left_value} {operator} {right_value} = {result}')
                    print(f"Logic compare operation ({operator}): {left_value} {operator} {right_value} = {result}")
                    return result
                else:
                    output.append('Logic compare operands not found')
                    print('Logic compare operands not found')
                    raise ValueError('Logic compare operands not found')
            else:
                output.append('Operator field not found')
                print('Operator field not found')
                raise ValueError('Operator field not found')
        elif block_type == 'math_arithmetic':
            operator_field = block.find('b:field[@name="OP"]', ns)
            if operator_field is not None:
                operator = operator_field.text
                left_block = block.find('b:value[@name="A"]/b:block', ns)
                right_block = block.find('b:value[@name="B"]/b:block', ns)
                if left_block is not None and right_block is not None:
                    left_value = execute_block(left_block, variables, output, statuses)
                    right_value = execute_block(right_block, variables, output, statuses)
                    if operator == 'ADD':
                        result = left_value + right_value
                    elif operator == 'MINUS':
                        result = left_value - right_value
                    elif operator == 'MULTIPLY':
                        result = left_value * right_value
                    elif operator == 'DIVIDE':
                        if right_value == 0:
                            raise ZeroDivisionError("Attempted division by zero")
                        result = left_value / right_value
                    output.append(f'Arithmetic operation ({operator}): {left_value} {operator} {right_value} = {result}')
                    print(f"Arithmetic operation ({operator}): {left_value} {operator} {right_value} = {result}")
                    return result
                else:
                    output.append('Arithmetic operands not found')
                    print('Arithmetic operands not found')
                    raise ValueError('Arithmetic operands not found')
            else:
                output.append('Operator field not found')
                print('Operator field not found')
                raise ValueError('Operator field not found')
        elif block_type == 'fetch_from_database':
            query = "SELECT * FROM test_table" 
            if not query:  # Simulate failure if the query is empty
                raise ValueError("Database query is empty")
            results = fetch_from_database(query)
            output.append(f'Database query result: {results}')
            print(f'Database query result: {results}')
            return results
        else:
            output.append(f'Unknown block type: {block_type}')
            print(f'Unknown block type: {block_type}')
            status = 'failure'
    except Exception as e:
        status = 'failure'
        print(f"Error executing block: {e}")
    finally:
        statuses[block.get('id')] = status

def execute_csv(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    output = []
    variables = {}
    statuses = {}
    ns = {'b': 'https://developers.google.com/blockly/xml'}
    print(f"Root tag: {root.tag}")
    for block in root.findall('b:block', ns):
        print(f"Found block: {ET.tostring(block, encoding='utf-8').decode('utf-8')}")
        result = execute_block(block, variables, output, statuses)
        output.append(f'Executed block: {block.get("type")} - Result: {result}')
        print(f'Executed block: {block.get("type")} - Result: {result}')
    if not output:
        output.append('No blocks executed.')
    return '\n'.join(output), statuses

def display_output(output):
    print("Displaying output in tkinter window")
    root = tk.Tk()
    root.title("Execution Output")

    text = tk.Text(root, wrap='word')
    text.pack(expand=True, fill='both')
    text.insert(tk.END, output)
    text.configure(state='disabled')  # Make the Text widget read-only

    root.mainloop()
    
if __name__ == "__main__":
    try:
        csv_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../csv_output/blockly_output.csv'))
        print(f"Reading CSV file: {csv_file_path}")
        if not os.path.exists(csv_file_path):
            print(f"CSV file does not exist: {csv_file_path}")
        output, statuses = execute_csv(csv_file_path)
        display_output(output)
        asyncio.run(notify_statuses(statuses))
    except Exception as e:
        print(f'An error occurred: {e}')
