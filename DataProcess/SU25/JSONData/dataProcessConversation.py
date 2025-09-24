import json
import csv

conversation_name = "conversation_conv_1750366972_20250619_140306"
inputFileName = conversation_name + ".json"
outputFileName = conversation_name + "_output.txt"
outcsvFileName = conversation_name + "telemetry_output.csv"
# Load the JSON file into a Python Dictionary
with open(inputFileName, 'r') as file:
    data = json.load(file)

# 'data' is now a Python dictionary
#w_file.write(data)

# Access dictionary data
# there are four parts of data in each conversation - 

# Part 1 - conversation ID data
# A conversation includes "conversation_id", "agent_id", and "timestamp"

with open(outputFileName, 'w') as w_file:

    w_file.write("*** Part 1 - Conversation ID Data *** \n")
    w_file.write(f"conversation_id: {data["conversation_id"]} \n")
    w_file.write(f"agent_id: {data["agent_id"]}\n")
    w_file.write(f"timestamp: {data["timestamp"]}\n")

# Part 2 - "prompts" 
# Each prompt is a user's input

    w_file.write("*** Part 2 - Prompts Info ***\n")
    prompts = data["prompts"]
    w_file.write(f"There are total {len(prompts)} prompts\n")
    count = 0
    for prompt in prompts:
        count += 1
        w_file.write(f" Prompts {count} : {prompt}\n")

# Part 3 - "responses"
# Each response includes a prompt, response and timestamp

    w_file.write("*** Part 3 - Responses Info ***\n")
    responses = data["responses"]
    w_file.write(f"There are total {len(responses)} responses\n")

    # Access dictionary data - how about the nested data
    w_file.write("=========== A example of a response ============\n")
    w_file.write(f"responses: prompt - {responses[0]["prompt"]}\n")
    w_file.write(f"responses: response - {responses[0]["response"]}\n")
    w_file.write(f"responses: timestamp - {responses[0]["timestamp"]}\n")

# for loop to w_file.write each object in the responses

    # how to use a nested loop to w_file.write each data (string)?
    outter_count = 0
    for response in responses:
        outter_count += 1
        w_file.write(f"===========Response {outter_count}   ============\n")
        inner_count = 0
        for item in response:
            inner_count += 1
            w_file.write(f"({inner_count}) {item}: {response[item]} \n")

# Part 4 - "telemetry"
# Each telemetry includes 5 attributes -- type, agent_id, timestamp, metadata, details
# metadata - the values in "details" is the first attributes
# 'thought' => context {'prompt' and 'conversation_id'} ** process user's prompt
# 'action_type' =>  {'action_type', 'action_input' (prompt), 'action_output' (none)} 
# 'tool_name' => {'tool_name', 'tool_input' (prompt), 'tool_output' (response)}
# details - 'thought', 'action_type', 'tool_name' 

    w_file.write("*** Part 4 - Telemetry Info ***\n")
    telemetrys = data["telemetry"]
    w_file.write(f"There are total {len(telemetrys)} telemetrys\n")

    # for loop to w_file.write each object in the responses

    outter_count = 0
    for telemetry in telemetrys:
        outter_count += 1
        w_file.write(f"===========Telemetry {outter_count}   ============\n")
        inner_count = 0
        for item in telemetry:
            inner_count += 1
            w_file.write(f"({inner_count}) {item}: {telemetry[item]} \n")


# create telemetry csv file - type, agent_id, timestamp, thought, action_type, tool_name, prompt, conversation_id, response
with open(outcsvFileName, 'w') as csv_file:
    fieldNames = ["type", "agent_id", "timestamp", "thought", "action_type", "tool_name", "prompt", "conversation_id", "response"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldNames)
    writer.writeheader()
    for telemetry in telemetrys:
        if telemetry["type"] == "thinking":
            writer.writerow({"type": telemetry["type"],  "agent_id": telemetry["agent_id"], "timestamp": telemetry["timestamp"], "thought": telemetry["details"]["thought"], "action_type": "none", "tool_name": "none", "prompt": telemetry["metadata"]["context"]["prompt"], "conversation_id": telemetry["metadata"]["context"]["conversation_id"], "response": "none"})
        elif telemetry["type"] == "action":
            writer.writerow({"type": telemetry["type"],  "agent_id": telemetry["agent_id"], "timestamp": telemetry["timestamp"], "thought": "none", "action_type": telemetry["details"]["action_type"], "tool_name": "none", "prompt": telemetry["metadata"]["action_input"], "conversation_id": "none", "response": telemetry["metadata"]["action_output"]})
        elif telemetry["type"] == "tool_use":
            writer.writerow({"type": telemetry["type"],  "agent_id": telemetry["agent_id"], "timestamp": telemetry["timestamp"], "thought": "none", "action_type": "none", "tool_name": telemetry["details"]["tool_name"], "prompt": telemetry["metadata"]["tool_input"], "conversation_id": "none", "response": telemetry["metadata"]["tool_output"]})
        else:
            writer.writerow({"type": telemetry["type"],  "agent_id": telemetry["agent_id"], "timestamp": telemetry["timestamp"], "thought": telemetry["details"], "action_type": telemetry["details"], "tool_name": telemetry["details"], "prompt": "none", "conversation_id": "none", "response": "none"})
print("********** program run correctly!!******")
print("read file from ", inputFileName)
print("text data written into, ", outputFileName)
print("telemetry data written into csv file, ", outcsvFileName )