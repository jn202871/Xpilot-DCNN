from ray_setup import setup_ray_cluster, list_files_in_directory, cleanup_remote_temp_files, create_cluster, shutdown_cluster
from ray_tasks import worker_task, manager_task, test_task, collect_xpilot_data, run_command, transfer_file
from parse import parse_data
import os
import ray
import getpass
import sys
import paramiko
import statistics
import torch
from dcnnretrain import retrain_dcnn, DCNNClassifier
from ray_tasks import save_scores_to_db
from clear import delete_data

def submit_jobs(worker_ips):
    """Submits a simulation job to all workers"""
    ray.init(address='auto', runtime_env={"working_dir": "./", "pip": ["paramiko", "pyvirtualdisplay", "asyncio", "aiofiles"]})
    worker_ids = range(1, len(worker_ips) + 1)
    results = [worker_task.options(resources={f"worker_{i+1}": 1}).remote(i+1) for i in range(len(worker_ips))]
    ray.get(results)
    
def submit_distributed_jobs(worker_ips):
    """
    Submits a distributed job to all workers, collects data, trains models,
    and repeats the process.
    """
    ray.init(address='auto', runtime_env={"working_dir": "./", "pip": ["paramiko", "pyvirtualdisplay", "asyncio", "aiofiles"]})
    run_command("cp ./Assets/Model.pt /tmp/Model.pt")
    for round_num in range(1, 5):  # 4 rounds (5)
        for sim_num in range(1, 11):  # 10 simulations per round (11)
            model = DCNNClassifier()
            model.load_state_dict(torch.load('/tmp/Model.pt'))
            model_ref = ray.put(model)
            if (round_num-1) % 2 == 0:
                results = [collect_xpilot_data.options(resources={f"worker": 1}, num_cpus=4).remote('expertBot', model_ref) for i in range(12)]
            else:
                results = [collect_xpilot_data.options(resources={f"worker": 1}, num_cpus=4).remote('fuzzyBot', model_ref) for i in range(12)]
            collected_data = ray.get(results)
        
            # Aggregate data and train new model
            aggregated_data = []
            score1_data = []
            score2_data = []
            for data in collected_data:
                aggregated_data.extend(data['lines'])
                score1_data.append(data['score1'])
                score2_data.append(data['score2'])
            
            with open('/tmp/aggregated_data.txt', 'w') as f:
                f.writelines(aggregated_data)
                
            save_scores_to_db(round_num,sim_num,1,statistics.mean(score1_data),statistics.mean(score2_data))
                
            parse_data(f"/tmp/aggregated_data.txt",f"/tmp/match_data.db")
            retrain_dcnn(f"/tmp/match_data.db",f"/tmp/Model.pt")
            
            delete_data(f"/tmp/match_data.db")
            run_command(f"rm /tmp/aggregated_data.txt")

    print("Distributed job completed.")
        
def test_cluster(worker_ips):
    """Submits a test job to all workers"""
    ray.init(address='auto', runtime_env={"working_dir": "./"})
    worker_ids = range(1, len(worker_ips) + 1)
    result_ids = [test_task.options(resources={f"worker_{i+1}": 1}).remote() for i in range(len(worker_ips))]
    results = ray.get(result_ids)
    for result in results:
        print(result)

def main():
    if len(sys.argv) != 2:
        print("Usage: python ray_launch.py [create|shutdown|submit|test]")
        sys.exit(1)
    username = 'jnash1'
    password = 'Ruggles72'
    head_ip = '136.244.224.34'
    IPLIST = [134, 61, 200, 45, 113, 187, 160, 145, 240, 41, 223, 88, 93, 229, 119, 15]
    IPHEADER = '136.244.224.'
    worker_ips = []
    for ip in IPLIST:
        worker_ips.append(f'{IPHEADER}{ip}')
    #'136.244.193.203', '136.244.193.167', '136.244.193.166', '136.244.193.153'
    #worker_ips = ['136.244.224.61']
    assets_directory = './Assets'
    files_to_transfer = list_files_in_directory(assets_directory)
    remote_dir = '/tmp'
    operation = sys.argv[1]

    if operation == 'create':
        create_cluster(username, password, head_ip, worker_ips, files_to_transfer, remote_dir)
    elif operation == 'shutdown':
        ray.init(address='auto')
        ray.shutdown()
        shutdown_cluster(username, password, worker_ips, assets_directory, remote_dir)
    elif operation == 'submit':
        submit_jobs(worker_ips)
    elif operation == 'submit_distributed':
        submit_distributed_jobs(worker_ips)
    elif operation == 'test':
        test_cluster(worker_ips)
    else:
        print("Invalid operation. Use 'create', 'shutdown', 'test', or 'submit'.")

if __name__ == "__main__":
    main()
