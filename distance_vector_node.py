from simulator.node import Node
import json
import copy

class Distance_Vector_Node(Node):
    def __init__(self, id):
        super().__init__(id)
        self.id = id
        #key : dest node, value: cost, path
        self.dv = {}
        
        self.seq = 1
        #seq number version of my own DV
        
        
        self.outbound_links = {}
        #link of my neighbors

        #key: the neighbor node, value: {"seq": seqnumber, "dv": {dv}}
        self.neighbor_dvs = {}
        
        
    def run_bellman_ford(self):

        #print("run_bellman_ford for id: ",self.id)
        
        #print("my dv before: ")
        
        #print(self.dv)
        
        #print("my neighbor_dvs: ")
        #print(self.neighbor_dvs)
        #copy_dv = copy.deepcopy(self.dv)
        
        
        #if self.dv == {}:
        #    self.dv = {self.id: (0, [])}
        self.dv = {}
        
        
        #if you are my neighbor but your not in my DV, add you to my dv, with path of just the nieghbor
        for neighbor in self.neighbors:
            if neighbor not in self.dv:
                self.dv[neighbor] = (self.outbound_links[neighbor],[neighbor])
            
        #dv should be updated with all nodes before fcn call
        for neighbor in self.neighbors:
            #print("for neighbor: ",neighbor)
            if neighbor not in self.neighbor_dvs:
                #print("neighbor not in neighbor dvs")
                #may need to add something
                
                continue
            
            neighbor_dv = self.neighbor_dvs[neighbor]["dv"]
            ##(0,[1,2,3])
            for dest, shortest_time_and_path in neighbor_dv.items():
                #new cost is going to this neighbor, and taking the nodes dv 
                #print('current dest: ',dest)
                new_cost = self.outbound_links[neighbor] + shortest_time_and_path[0]
                #print('new cost: ',new_cost)
                # check if im in the path, ignore if im in
                if self.id in shortest_time_and_path[1]:
                    continue
                
                if dest not in self.dv:
                    #print("dest didnt exist in dv, adding...")
                    path = copy.deepcopy(shortest_time_and_path[1])
                    path = [neighbor] + path
                    self.dv[dest] = (new_cost, path)
                else:  
                    #print("current cost: ", self.dv[dest][0])
                    #if the new cost is faster than the cost I have in my dv and that I am not in the path
                    
                    if new_cost < self.dv[dest][0]:
                        #print(shortest_time_and_path[1])
                        #print(self.id)
                        #print("new cost cheaper")
                        #input()
                        #add the node to the front of the path, update my dv path, and the new cost
                        path = copy.deepcopy(shortest_time_and_path[1])
                        path = [neighbor] + path
                        #seq = value[0] + 1
                        self.dv[dest] = (new_cost, path)
                    else:
                        #print("no need for change")
                        pass

        '''package = {'seq': self.seq, 
                   'dv': self.dv, 
                   'id': self.id}
        
        
        #print("my dv after: ")
        
        #print(self.dv)
        
        print("LINK HAS BEEN UPDATED, BROADCASTING TO", self.neighbors)
        self.send_to_neighbors(json.dumps(package))

        self.seq += 1'''
        
        #time.sleep(0.5)




                

    # Return a string
    def __str__(self):
        return "Rewrite this function to define your node dump printout"

    # Fill in this function
    def link_has_been_updated(self, neighbor, latency):
        # latency = -1 if delete a link
        # update dv if new shortest path
        #print("link_has_been_updated for ",self.id)
    
        #print("new neighbor:",neighbor)
        #print("new latency:",latency)
        
        if latency == -1 and neighbor in self.neighbors:
            #print("removing")
            self.neighbors.remove(neighbor)
            
            del self.outbound_links[neighbor]
            del self.neighbor_dvs[neighbor]
            
            ### GO THROUGH OWN DISTANCE VECTOR AND CHECK IF the DELETED LINK IS UTILIZED IN ANY SHORTEST PATHS IN MY DV
            ### TO DO THIS, SIMPLY CHECK THE NEXT HOP OF ALL MY DESTINATIONS AND SEE IF THEY ARE USING THIS LINK
            
            new_dv = {}
            for i in self.dv.keys():
                if neighbor != self.get_next_hop(i):
                    new_dv[neighbor] = self.dv[neighbor]
            self.dv = new_dv
            
        else:
            if neighbor not in self.neighbors:
                self.neighbors.append(neighbor)
                # self.neighbor_dvs[neighbor] = {neighbor: (0, latency, [neighbor])}


            # self.dv[neighbor] = (0, latency, [neighbor])
        
        
            self.outbound_links[neighbor] = latency
        
        #if latency != -1:
        #    self.dv[neighbor] = (latency, [neighbor])
        #self.neighbor_dvs = {}
        #input()
        
        #recalculate my own DV from scratch
        #if neighbor in self.dv:
        #    del self.dv[neighbor]
        
        #self.dv = {}
        #Should I forget all my neighbor DV's as well?
        #self.neighbor_dvs = {}
        
        
        ###TWO SCENARIOS WHERE BROADCASTING IS REQUIREED
        # 1. LINK HAS BEEN UPDATED
        # 2. DV CHANGED (from a broadcast)
        self.run_bellman_ford()
        
        package = {'seq': self.seq, 
                   'dv': self.dv, 
                   'id': self.id}
        
        #print("LINK HAS BEEN UPDATED, BROADCASTING TO", self.neighbors)
        self.send_to_neighbors(json.dumps(package))

        self.seq += 1
            

    # Fill in this function
    def process_incoming_routing_message(self, m):
        copy_dv = copy.deepcopy(self.dv)
        
       #print("process_incoming_routing_message for: ",self.id)
        msg = json.loads(m)
        seq = int(msg['seq'])
        id = int(msg['id'])
        neighbor_dv = msg['dv']
        new_neighbor_dv = {}
        for key,value in neighbor_dv.items():
            new_neighbor_dv[int(key)] = value
        
        
        #print(new_neighbor_dv)
        
        
        

        if id not in self.neighbor_dvs.keys():
            # this is a new neighbordb
            self.neighbor_dvs[id] = {"seq": seq, "dv": new_neighbor_dv}
            #print("this is a new neighbordb")
        else:
            if (seq > self.neighbor_dvs[id]["seq"]):
                #print("this is a new seq")
                self.neighbor_dvs[id]["seq"] = seq
                self.neighbor_dvs[id]['dv'] = new_neighbor_dv
            
            
        #print("running bf")
        
        self.run_bellman_ford()
        package = {'seq': self.seq, 
                   'dv': self.dv, 
                   'id': self.id}
        
        
        #print("my dv after: ")
        
        #print(self.dv)
        if copy_dv != self.dv:
            #print("DV HAS BEEN UPDATED, BROADCASTING TO", self.neighbors)
            self.send_to_neighbors(json.dumps(package))

            self.seq += 1
        
        

        

    # Return a neighbor, -1 if no path to destination
    def get_next_hop(self, destination):

        if destination in self.dv:
            return self.dv[destination][1][0]
        
        return -1
