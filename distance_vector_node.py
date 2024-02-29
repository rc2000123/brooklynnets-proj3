from simulator.node import Node
import json
import copy


class Distance_Vector_Node(Node):
    def __init__(self, id):
        super().__init__(id)
        self.id = id
        #key : dest node, value: seq, cost, path
        self.dv = {id: (0, 0, [])}
        self.seq = 1
        self.received_seq = {}

        self.outbound_links = {}


        #key: the destination node, value: sequence, cost, path
        self.neighbor_dvs = {}
        
        
    def run_bellman_ford(self):
        copy_dv = copy.deepcopy(self.dv)
        #dv should be updated with all nodes before fcn call
        for neighbor in self.neighbors:
            if neighbor not in self.neighbor_dvs:
                continue
            dv = self.neighbor_dvs[neighbor]

            for node, value in dv.items():
                new_cost = self.outbound_links[node] + value[1]
                if new_cost < self.dv[neighbor][1] and self.id not in value[2]:
                    path = copy.deepcopy(value[2])
                    path = path.insert(0, node)
                    seq = value[0] + 1
                    self.dv[node] = (seq, new_cost, path)

        package = {'seq': self.seq, 
                   'dv': self.dv, 
                   'id': self.id}
        print(copy_dv, self.dv)
        if self.dv != copy_dv:
            self.send_to_neighbors(json.dumps(package))

            self.seq += 1




                

    # Return a string
    def __str__(self):
        return "Rewrite this function to define your node dump printout"

    # Fill in this function
    def link_has_been_updated(self, neighbor, latency):
        # latency = -1 if delete a link
        # update dv if new shortest path

        if latency == -1 and neighbor in self.neighbors:

            self.neighbors.remove(neighbor)
            del self.dv[neighbor]
            del self.outbound_links[neighbor]
            
        else:
            if neighbor not in self.neighbors:
                self.neighbors.append(neighbor)
                # self.neighbor_dvs[neighbor] = {neighbor: (0, latency, [neighbor])}
                self.dv[neighbor] = (0, latency, [neighbor])
               
            else:
                self.dv[neighbor] = (0, latency, [neighbor])

            # self.dv[neighbor] = (0, latency, [neighbor])
            self.outbound_links[neighbor] = latency

        print(self.id, self.neighbors, self.neighbor_dvs)
                    
        self.run_bellman_ford()
            

    # Fill in this function
    def process_incoming_routing_message(self, m):
        neighbor_dv = json.loads(m)
        seq = neighbor_dv['seq']
        id = neighbor_dv['id']

        if id in self.received_seq and seq > self.received_seq[id]:
            self.neighbor_dvs[id] = neighbor_dv['dv']
            self.received_seq[id] = seq

        print("running bf")
        self.run_bellman_ford()

        

    # Return a neighbor, -1 if no path to destination
    def get_next_hop(self, destination):

        if destination in self.dv:
            return self.dv[destination][2][0]
        
        return -1
