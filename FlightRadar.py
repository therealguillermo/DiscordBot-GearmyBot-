import discord
from discord.ext import commands
import asyncio
from FlightRadar24.api import FlightRadar24API


MY_COORDS = (40.794525,-77.911416) 


class FlightRadar(commands.Cog):
    def __init__(self, Client):
        self.client = Client
        self.fAPI = FlightRadar24API()
        self.iter = 0
        print("Starting Up FlightRadar")

    def getClosestFlight(self):
        print(f"times iter: {self.iter}")
        tl_y = MY_COORDS[0] + .001*self.iter
        br_y = MY_COORDS[0] - .001*self.iter
        tl_x = MY_COORDS[1] + .001*self.iter
        br_x = MY_COORDS[1] - .001*self.iter
        print(f"{tl_y}, {br_y}, {tl_x}, {br_x}\n")
        zone = {"tl_y": round(tl_y, 6), "br_y": round(br_y, 6), 
                "tl_x": round(tl_x, 6), "br_x": round(br_x, 6)}
        #zone = self.fAPI.get_zones()['northamerica']
        bounds = self.fAPI.get_bounds(zone)
        flights = self.fAPI.get_flights(bounds=bounds)
        if len(flights) == 0:
            self.iter += 1
            return self.getClosestFlight()
        elif len(flights) > 1:
            return flights
        else:
            return flights[0]

    @commands.command()
    async def closestFlight(self, ctx):
        print(self.fAPI.get_zones()['northamerica'])
        closestFlight = self.getClosestFlight() 
        print(f'flight: {closestFlight}')
        self.iter = 0

async def setup(client):
    await client.add_cog(FlightRadar(client))

