from simulator.node import Node
import json


class Distance_Vector_Node(Node):
    def __init__(self, id):
        super().__init__(id)

         #key: the destination node, value: sequence, cost, dv
        self.dvs = {}
        
        ## A ROUNTING TABLE SHOULD ASSUME A LINK IN BETWEEN EVERY OTHER NODE (CONNECTED OR NOT IF NOT CONNECTED, SET LATENCY TO -1)
        
        #"c": link(a->b)
        
        #pair of nodes <a<->b>(frozenset)| (seq numbers, latency)
        #--------------
        #  c    a->b
        #  d    a->b 
        
        
        

    # Return a string
    def __str__(self):
        return "Rewrite this function to define your node dump printout"

    # Fill in this function
    def link_has_been_updated(self, neighbor, latency):
        # latency = -1 if delete a link
        # update dv if new shortest path
        if latency == -1 and neighbor in self.neighbors:

            self.neighbors.remove(neighbor)
            
        else:
            if neighbor not in self.neighbors:
                self.neighbors.append(neighbor)
                # for link_frozenset,value in self.dvs.items():
                #     list_frozenset = list(link_frozenset)
                #     broadcast_msg = {
                #         "src_id": list_frozenset[0],
                #         "dst_id": list_frozenset[1],
                #         "new_latency": value[0],
                #         "new_seq_num": value[1]
                #     }

                if neighbor in self.dvs:
                    if self.dvs[neighbor][0] > latency:
                        new_seq_num =
                        self.dvs[neighbor] = (latency, [neighbor])
                
                    

                self.send_to_neighbors(json.dumps(self.dvs))

                new_seq_num = 0

                if 
                    
        



        pass

    # Fill in this function
    def process_incoming_routing_message(self, m):
        pass

    # Return a neighbor, -1 if no path to destination
    def get_next_hop(self, destination):
        return -1
