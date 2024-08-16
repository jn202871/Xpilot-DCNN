import subprocess
import ray
import time
import socket
import sys
import paramiko
import sqlite3
import os
import torch
from clear import delete_data
from parse import parse_data
from dcnnretrain import retrain_dcnn, DCNNClassifier
from pyvirtualdisplay import Display

@ray.remote
def test_task():
    """Test task"""
    return f"Task executed on: {socket.gethostname()}"
    
@ray.remote
def collect_xpilot_data(opponent, model):
    """
    Collects data by running a single simulation with the specified opponent and model.
    Returns the collected data, score, etc. to the main task.
    """
    prep_commands = ["chmod +x /tmp/xpilots", "chmod +x /tmp/xpilot", "pkill -9 xpilots"]
    for cmd in prep_commands:
        run_command(cmd)

    xpilot_command = "/tmp/xpilots -map /tmp/lifeless.xp -switchBase 1 -maxRoundTime 30 >/dev/null 2>&1 &"
    run_command(xpilot_command)
    
    torch.save(model.state_dict(), '/tmp/Model.pt')

    bot_commands = [
        ("timeout 10m python3 /tmp/expertAgent.py", "timeout 10m python3 /tmp/DCNNAgent.py"),
        ("timeout 10m python3 /tmp/fuzzyAgent.py", "timeout 10m python3 /tmp/DCNNAgent.py")
    ]
    with Display(visible=0, size=(1920, 1080)):
        if opponent == 'expertBot':
            for cmd in bot_commands[0]:
                    run_command(f"{cmd} >/dev/null 2>&1 &")
        else:
            for cmd in bot_commands[1]:
                    run_command(f"{cmd} >/dev/null 2>&1 &")
        time.sleep(610)

    data = {}
    try:
        with open('/tmp/score1.txt', 'r') as file:
            try:
                score1 = float(file.readlines()[-1].strip())
            except:
                score1 = 0.0
            print(score1)
        with open('/tmp/score2.txt', 'r') as file:
            try:
                score2 = float(file.readlines()[-1].strip())
            except:
                score2 = 0.0
            print(score2)
        with open('/tmp/data.txt', 'r') as file:
            lines = file.readlines()   
            print(f"Worker data file length:", len(lines))
        
        data['score1'] = score1
        data['score2'] = score2
        data['lines'] = lines
    finally:
        run_command("echo 0.0 > /tmp/score1.txt")
        run_command("echo 0.0 > /tmp/score2.txt")
        run_command("rm /tmp/data.txt")
        run_command("rm /tmp/Model.pt")
    
    return data
    
@ray.remote
def worker_task(worker_id):
    """Main simulation task that works as follows:
       1. launch xpilots server
       2. start first sim (bots change out depending on the round number)
       3. transfer files back to the manager (data and current model)
       4. call manager function to update model
       5. manager updates model and records scores, then transfers new model to worker
       6. worker continues until all rounds are complete"""
    prep_commands = ["chmod +x /tmp/xpilots", "chmod +x /tmp/xpilot", "pkill -9 xpilots"]
    for cmd in prep_commands:
        run_command(cmd)
    xpilot_command = "/tmp/xpilots -map /tmp/lifeless.xp -switchBase 1 -maxRoundTime 30 >/dev/null 2>&1 &"
    #run_command(xpilot_command)
    bot_commands = [
        ("timeout 20m python3 /tmp/expertAgent.py", "timeout 20m python3 /tmp/DCNNAgent.py"),
        ("timeout 20m python3 /tmp/fuzzyAgent.py", "timeout 20m python3 /tmp/DCNNAgent.py")
    ]
    with Display(visible=0, size=(1920,1080)):
        # Execute the task cycles
        for round_num in range(1, 5):  # 4 rounds (5)
            for sim_num in range(1, 11):  # 10 simulations per round (11)
                run_command(xpilot_command)
                # Run bot commands and parse
                bot_ids = []
                for cmd in bot_commands[(round_num - 1) % 2]:
                    run_command(f"{cmd} >/dev/null 2>&1 &")
                time.sleep(1220)  # Wait for bots to finish
                try:
	                transfer_file('jnash', 'Ruggles72', '136.244.224.34', '/tmp/data.txt', f"/tmp/data_{worker_id}.txt")
	                transfer_file('jnash', 'Ruggles72', '136.244.224.34', '/tmp/Model.pt', f"/tmp/Model_{worker_id}.pt")
	                with open('/tmp/score1.txt', 'r') as file:
	                    try:
	                        score1 = float(file.readlines()[-1].strip())
	                    except:
	                        score1 = 0.0
	                    print(score1)
	                with open('/tmp/score2.txt', 'r') as file:
	                    try:
	                        score2 = float(file.readlines()[-1].strip())
	                    except:
	                        score2 = 0.0
	                    print(score2)
	                with open('/tmp/data.txt', 'r') as file:
	                    lines = file.readlines()   
	                    print(f"Worker_{worker_id} data file length:", len(lines))
	                
	                # Update model based on manager's response
	                ray.get(manager_task.remote([score1, score2], worker_id, round_num, sim_num))
                finally:
                    # Clear local data
                    run_command("echo 0.0 > /tmp/score1.txt")
                    run_command("echo 0.0 > /tmp/score2.txt")
                    run_command("rm /tmp/data.txt")

    return f"All Runs Complete On Worker {worker_id}"

@ray.remote(resources={"manager_resource": 1}, num_gpus=1)
def manager_task(scores, worker_id, round_num, sim_num):
    """Manager task to retrain worker models and save scores to db"""
    worker_ips = ['136.244.224.61','136.244.224.58','136.244.224.145','136.244.224.240', '136.244.224.223', '136.244.224.229', '136.244.224.41', '136.244.224.88', '136.244.224.200', '136.244.224.230', '136.244.224.45', '136.244.224.187', '136.244.224.224']
    parse_data(f"/tmp/data_{worker_id}.txt",f"/tmp/match_data_{worker_id}.db")
    retrain_dcnn(f"/tmp/match_data_{worker_id}.db",f"/tmp/Model_{worker_id}.pt")
    run_command(f"rm /tmp/match_data_{worker_id}.db")
    run_command(f"rm /tmp/data_{worker_id}.txt")
    save_scores_to_db(round_num, sim_num, worker_id, scores[0], scores[1])
    transfer_file('jnash1', 'Ruggles72', worker_ips[worker_id-1], f"/tmp/Model_{worker_id}.pt", '/tmp/Model.pt')
    return

def run_command(command):
    """Helper function to run a command"""
    return_code = os.system(command)
    if return_code != 0:
        print(f"Command failed with return code: {return_code}")
        print(f"Failed command: {command}")

        
def transfer_file(username, password, hostname, local_file, remote_path):
    """Transfer a single file to a remote machine via SFTP."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, username=username, password=password)
    sftp = client.open_sftp()
    sftp.put(local_file, remote_path)
    
    sftp.close()
    client.close()
    
def wrap_xvfb(command):
    """Prepends xvfb-run to commands that require an X environment"""
    return f"xvfb-run --auto-servernum --server-args='-screen 0 1960x1080x24' {command}"
    
def save_scores_to_db(round_num, sim_num, worker_id, score1, score2):
    """Manager helper func to save scores to db"""
    conn = sqlite3.connect('/home/jnash/Research/Xpilot-Ray/ray_scores.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            round_number INTEGER,
            sim_number INTEGER,
            worker_id INTEGER,
            Bot REAL,
            DCNN REAL
        )
    ''')
    c.execute('INSERT INTO scores (round_number, sim_number, worker_id, Bot, DCNN) VALUES (?, ?, ?, ?, ?)',
              (round_num, sim_num, worker_id, score1, score2))
    conn.commit()
    conn.close()
