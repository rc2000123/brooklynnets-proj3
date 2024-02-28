from simulator.node import Node
import json


class Distance_Vector_Node(Node):
    def __init__(self, id):
        super().__init__(id)

        #key : dest node, value: seq, cost, path
        self.dv = {id: (0, 0, [])}

        #key: the destination node, value: sequence, cost, path
        self.dvs = {}
        
        
    def run_bellman_ford(self):
        temp_dv = {}
        for each v in self.dv.keys():
            if v

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
            
        else:
            if neighbor not in self.neighbors:
                self.neighbors.append(neighbor)
               

            self.dv[neighbor] = (0, latency, [neighbor])
                    
            self.run_bellman_ford()
            

    # Fill in this function
    def process_incoming_routing_message(self, m):
        

    # Return a neighbor, -1 if no path to destination
    def get_next_hop(self, destination):

        if destination in self.dv:
            return self.dv[destination][2][0]
        
        return -1
