import psutil
from datetime import datetime
import graphviz

def get_process_info(process):
    try:
        create_time = datetime.fromtimestamp(process.create_time()).strftime("%Y-%m-%d %H:%M:%S")
        return {
            "pid": process.pid,
            "name": process.name(),
            "create_time": create_time,
            "children": []
        }
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return None

def build_process_tree():
    processes = {}
    for proc in psutil.process_iter(['pid', 'ppid', 'name', 'create_time']):
        try:
            proc_info = get_process_info(proc)
            if proc_info:
                processes[proc.pid] = proc_info
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    root = {"pid": 0, "name": "System", "children": []}

    for pid, proc_info in processes.items():
        try:
            parent = psutil.Process(pid).parent()
            if parent:
                parent_pid = parent.pid
                if parent_pid in processes:
                    processes[parent_pid]["children"].append(proc_info)
                else:
                    root["children"].append(proc_info)
            else:
                root["children"].append(proc_info)
        except psutil.NoSuchProcess:
            root["children"].append(proc_info)

    return root

def create_graph(node, graph=None):
    if graph is None:
        graph = graphviz.Digraph(comment='Process Tree')
        graph.attr(rankdir='LR')

    node_id = f"{node['pid']}_{node['name']}"
    label = f"{node['name']}\\nPID: {node['pid']}\\nCreated: {node.get('create_time', 'N/A')}"
    graph.node(node_id, label)

    for child in node["children"]:
        child_id = f"{child['pid']}_{child['name']}"
        graph.edge(node_id, child_id)
        create_graph(child, graph)

    return graph

if __name__ == "__main__":
    process_tree = build_process_tree()
    graph = create_graph(process_tree)
    graph.render('process_tree', format='png', cleanup=True)
    print("Process tree visualization saved as 'process_tree.png'")