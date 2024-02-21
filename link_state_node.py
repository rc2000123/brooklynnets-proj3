from simulator.node import Node
import json

class Link_State_Node(Node):
    def __init__(self, id):
        super().__init__(id)
        
        
        #key: the destination node, value: the outgoing link
        self.routing_table = {}
        
        ## A ROUNTING TABLE SHOULD ASSUME A LINK IN BETWEEN EVERY OTHER NODE (CONNECTED OR NOT IF NOT CONNECTED, SET LATENCY TO -1)
        
        #"c": link(a->b)
        
        #pair of nodes <a<->b>(frozenset)| (seq numbers, latency)
        #--------------
        #  c    a->b
        #  d    a->b 
        
        
        ##we should maintian a links table (of reachable nodes) that will be populated by flooding, where the key is a frozen set of  src<->dest
        ##value is [latency,seq_num]
        #self.links  = {}
        
        #a->b->c
        
        
        #keep track of all nodes?
        #self.all_nodes = []
        
        #
        


        
    # Return a string
    def __str__(self):
        return "Rewrite this function to define your node dump printout"

    def get_routing_table(self):
        return self.routing_table
        
        return super().get_routing_table()
    # Fill in this function
    def link_has_been_updated(self, neighbor, latency):
        #neighbor is id
        # latency = -1 if delete a link
        if latency == -1 and neighbor in self.neighbors:

            self.neighbors.remove(neighbor)
            
        else:
            self.neighbors.append(neighbor)
        
           
            
        #UPDATE ROUTING TABLE
        ##IF the new link was not in my router table previously, create a new item in the routing table, with seq number 0
        ###BROADCAST A MESSAGE regarding the updated LINK, and the new latency and incremented sequence number###
        
        #self.send_to_neighbor(neighbor, "hello")
        
        #create a frozenset of yourself and your neighbor
        link_frozenset = frozenset([self.id,neighbor])
        
        new_seq_num = 0
        
        if link_frozenset in self.routing_table:
            #old link, but new latency, update to new value, and increment seq  number
            pre_seq_number = self.routing_table[link_frozenset][1]
            new_seq_num = pre_seq_number + 1
        
        #update/add to routing table, and also make a copy for the other frozenset    
        self.routing_table[link_frozenset] = (latency,new_seq_num)
        self.routing_table[frozenset([neighbor,self.id])] = (latency,new_seq_num)
        
        
        ##MAYBE I SHOULD SEND ALL TABLES INSTEAD
        broadcast_msg = {
            "src_id": self.id,
            "dst_id": neighbor,
            "new_latency": latency,
            "new_seq_num": new_seq_num
        }
        
        self.send_to_neighbors(json.dumps(broadcast_msg))
        
        self.logging.debug('link update, neighbor %d, latency %d, time %d' % (neighbor, latency, self.get_time()))

    # Fill in this function
    def process_incoming_routing_message(self, m):
        ###RECEIVE A MESSAGE regarding the updated LINK, and the new latency and sequence number###
        
        ###CHECK IF SEQ NUMBER is newer, if so, update my own routing table###
        ###and then broadcast to my neighbors
        recv_msg = json.loads(m)
        
        print("Node:",self.id,"Recieved message: ",recv_msg)
        
        
        #Check if neighbor changed, and make updates
        if recv_msg['src_id'] == self.id or recv_msg['dst_id'] == self.id:
            neighbor = 0
            if recv_msg['src_id'] == self.id :
                neighbor = recv_msg['dst_id']
            else:
                neighbor = recv_msg['src_id']
        
            if recv_msg["new_latency"] == -1 and neighbor in self.neighbors:
                self.neighbors.remove(neighbor)
            else:
                self.neighbors.append(neighbor)
        
        
        link_frozenset = frozenset([recv_msg["src_id"],recv_msg["dst_id"]])
        
        new_seq_num = 0
        
        if link_frozenset in self.routing_table:
            if recv_msg["new_seq_num"] > self.routing_table[link_frozenset][1]:
                new_seq_num = recv_msg["new_seq_num"]
                
            else:
                #this is an older version, disregard it, dont send to other people
                return
        
        #update routing table (for both ends)
        self.routing_table[link_frozenset] = (recv_msg["new_latency"],new_seq_num)
        self.routing_table[frozenset([recv_msg["dst_id"],recv_msg["src_id"]])] = (recv_msg["new_latency"],new_seq_num)
        
        #pass the message down
        self.send_to_neighbors(m)

    # Return a neighbor, -1 if no path to destination
    
    def get_next_hop(self, destination):
        
        print("get_next_hop")
        print("self is ", self.id)
        print("target dest is ", destination)
        print(self.routing_table)
        ####RUN DIJKSTRAS HERE
        #### GET A LIST OF SHORTEST PATH DISTANCES, and its corresponding path TO EVERY DEST
        ### RETURN THE NODE THAT IT SHOULD GO TO IN THE SHORTES PATH
        sptSet = []
        
        #create a dist_dict to keep track of the shortest path, and the path itself to it
        dist_dict = {}
        
        for link in self.routing_table.keys():
            link = list(link)
            dist_dict[link[0]] = (float('inf'),[])
            dist_dict[link[1]] = (float('inf'),[])
        
        dist_dict[self.id] = (0,[])
        
        
        
        while True:
            #min_key, min_value = min(dist_dict.items(), key=lambda x: x[1][0])
            
            min_node = None
            min_value = float('inf')
            for node in dist_dict.keys():
                print(dist_dict[node])
                if dist_dict[node][0] < min_value and (node not in sptSet):
                    min_value = dist_dict[node][0]
                    min_node = node
            
            if min_node == None:
                print("no node found")
                return -1
            
            if min_node == destination:
                #popped destination value, so just return path
                
                print("found, next hop is: ", dist_dict[min_node][1])
                return dist_dict[min_node][1][0]
            
            
            sptSet.append(min_node)
            
            for pair in self.routing_table.keys():
                if min_node in pair:
                    dest_node = None
                    list_pair = list(pair)
                    if min_node == list_pair[0]:
                        dest_node = list_pair[1]
                    else:
                        dest_node = list_pair[0]  
                    
                    if dist_dict[min_node][0] + self.routing_table[pair][0] < dist_dict[dest_node][0]:
                        #update the dist_dict to new distance, and next value to hop to 
                        
                        ##if next hop is uninit, populate it, otherwise just update shorest path
                        
                        dist_dict[dest_node] = (dist_dict[min_node][0] + self.routing_table[pair][0], dist_dict[min_node][1] + [dest_node])
                        
                        
                        #if dist_dict[dest_node][1] == -1:
                        #    dist_dict[dest_node] = (dist_dict[min_node][0] + self.routing_table[pair][1],dest_node)
                        #else:
                            
                        #    dist_dict[dest_node] = (dist_dict[min_node][0] + self.routing_table[pair][1],dist_dict[dest_node][1])
                            
                
            
            
        
        
        
        return -1
