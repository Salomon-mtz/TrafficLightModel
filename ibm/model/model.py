import mesa
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from .agents import TrafficLight, Vehicle, SideWalk, Building
from mesa.time import RandomActivation


class TrafficModel(mesa.Model):
    def __init__(self, nVehicles=4, nLights=4, nSize=16, percent_pesero=0.2, nSideWalk=86, nBuild = 16):
        super().__init__()
        self.num_vehicles = nVehicles
        self.num_lights = nLights
        self.num_side = nSideWalk
        self.num_buildings = nBuild
        self.size = nSize
        self.grid = MultiGrid(nSize, nSize, False)
        self.schedule = RandomActivation(self)
        self.counter = 0

        self.collisions = 0
        self.percent_pesero = percent_pesero


        origin_pos = [[8, 0], [0, 7], [7, 15], [15, 8]]
        self.next_to_origin = {
            (8, 0): [0, 1, 8, 1],
            (0, 7): [1, 0, 1, 7],
            (7, 15): [0, -1, 7, 14],
            (15, 8): [-1, 0, 14, 8]
        }
        orient = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        
   

        
        # Create Vehicles
        for i in range(self.num_vehicles):
            rand = self.random.randint(0, 3)
            x1 = origin_pos[rand][0]
            y1 = origin_pos[rand][1]
            x2 = orient[rand][0]
            y2 = orient[rand][1]

            # pesero vehicles
            v = Vehicle(i, (x1, y1), (x2, y2), self.percent_pesero, self)
            self.grid.place_agent(v, (x1, y1))
            self.schedule.add(v)

        pos_lig = [[6, 7], [7, 9], [8, 6], [9, 8]]
        pos_side = [[6, 9], [5, 9], [4, 9], [3, 9], [2,9], [1,9], [6,10], [6,11], [6,12], [6,13],[6,14],
                    [9,9], [10,9], [11,9],[12,9],[13,9],[14,9],[9,10], [9,11], [9,12], [9,13],[9,14],
                    [6, 6], [6, 5], [6, 4], [6, 3], [6,2], [6,1],
                    [6, 6], [5, 6], [4, 6], [3, 6], [2,6], [1,6],
                    [9, 6], [10, 6], [11, 6], [12, 6], [13,6], [14,6],
                    [9, 5], [9, 4], [9, 3], [9, 2], [9,1],
                    [6, 14], [5, 14], [4, 14], [3, 14], [2,14], [1,14],
                    [1,10], [1,11], [1,12], [1,13],[1,14],
                    [10, 14], [11, 14], [12, 14], [13, 14], [14,14],
                    [14,10], [14,11], [14,12], [14,13],[14,14],  #66
                    [1,5], [1,4], [1,3], [1,2],[1,1],
                    [1,1], [2,1], [3,1], [4,1],[5,1],#76
                    [10,1], [11,1], [12,1], [13,1],[14,1],
                    [14,2], [14,3], [14,4], [14,5],[14,6],] 

        pos_img = [[3, 12], [4, 12], [3, 11], [4, 11],
                    [11, 12], [12, 12], [11, 11], [12, 11],
                    [11, 4], [12, 4], [11, 3], [12, 3],
                    [3, 4], [4, 4], [3, 3], [4, 3],]
                    
        count = 0
        count2 = 0
        count3 = 0

        # Create TrafficLights
        for i in range(self.num_vehicles, self.num_vehicles + self.num_lights):
            x = pos_lig[count][0]
            y = pos_lig[count][1]
            t = TrafficLight(i, (x, y), self)
            count += 1
            self.grid.place_agent(t, (x, y))
            self.schedule.add(t)

        # Create SideWalk
        for i in range(self.num_vehicles, self.num_vehicles + self.num_side):
            x = pos_side[count2][0]
            y = pos_side[count2][1]
            s = SideWalk(x,y)
            count2 += 1
            self.grid.place_agent(s, (x, y))
            #self.schedule.add(s)

        # Create building
        for i in range(self.num_vehicles, self.num_vehicles + self.num_buildings):
            x = pos_img[count3][0]
            y = pos_img[count3][1]
            b = Building(x,y)
            count3 += 1
            self.grid.place_agent(b, (x, y))
            #self.schedule.add(s)

    def crash_count(self):
        crashes = 0
        for i in range(self.num_vehicles):
            for j in range(self.num_vehicles):
                agent = self.schedule.agents[i]
                agent2 = self.schedule.agents[j]
                if agent.pos == agent2.pos:
                    crashes += 1
                    print(crashes)

    def count_directions(self):
        total_agents = []

        for i in range(self.num_vehicles):
            agent = self.schedule.agents[i]

            # Add to total agents
            total_agents.append(agent.change_direction)

        return total_agents



        # Advances the model by one step
    def step(self):
        self.counter += 1
        self.schedule.step()

        positions = []
        for i in range(self.num_vehicles):
            car_id = self.schedule.agents[i].unique_id
            xy = self.schedule.agents[i].pos
            bus = self.schedule.agents[i].pesero
            p = [car_id,
                 xy[0]*9,
                 5,
                 xy[1]*9,
                 bus
                 ]
            positions.append(p)

        light_states = []
        for i in range(self.num_vehicles, self.num_vehicles + self.num_lights):
            light_id = self.schedule.agents[i].unique_id
            state = self.schedule.agents[i].state

            s = [light_id,
                 state
                 ]

            light_states.append(state)


        return positions, light_states

    def run_model(self, step=20):
        for i in range(step):
            self.step()
