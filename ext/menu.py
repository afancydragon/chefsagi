#####################################################################################
#               scheduled menu creation
#           
#####################################################################################
import os
import discord
import datetime
from discord.ext import commands
import json


menudb = './menus/' #path to menu folder

#Alias lists
dowalias = ['monday', 'Tuesday', 'tuesday', 'Wednesday', 'wednesday',
'Thursday', 'thursday', 'Friday', 'friday', 'Saturday', 'saturday','Sunday','sunday']
destructionalias = ['clear','Destroy', 'destroy', 'Nuke','nuke','Remove','remove','Snap','snap']
menualias = ['menu','Plan','plan','thedeetsplease']
weekalias = ['Schedule','schedule','week','Week']
assignmentalias = ['give','Assign','assign','Reassign','reassign']

#case insensitive lists
chefnames = ['robosouschef','chefsagi','robochef','sagi']

#weird date ordinal, terrible thing
ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])


#default json block
item = 'None'
person = 'None'
menweek = {
    'monday': [item, person],
    'tuesday': [item, person],
    'wednesday': [item, person],
    'thursday': [item, person],
    'friday': [item, person],
    'saturday': [item, person],
    'sunday': [item, person]}


class Menu_Management(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def chmen(self,ctx):
        guildloc = menudb + f'{ctx.message.guild.id}' + '/'
        print(guildloc)
        check = dict()
        check['newmenflag'] = 0
        currentday = datetime.date.today()
        year, week_num, day_of_week = currentday.isocalendar()
        check['menpath'] = (guildloc + f'{str(year) + str(week_num)}.cheffile')
        print(check['menpath'])
        if(os.path.exists(check['menpath']) == False):
            check['newmenflag']  = 1
            os.makedirs(guildloc, exist_ok=True)
            menufile = open(check['menpath'],'w')
            menufile.write(json.dumps(menweek))
            menufile.close
        menufile = open(check['menpath'], 'r')
        check['mendata'] = json.loads(menufile.read())
        menufile.close
        return check

    def nickcheck(self, ctx):
        if(ctx.message.author.nick == None):
            return ctx.message.author.name
        else:
            return ctx.message.author.nick

    def itemprep(self, itemraw):
        itemparse = ''
        for m in itemraw:
            itemparse = itemparse + ' ' + m     
        return itemparse.lstrip()

    def eggcheckmenu(self, ctx, itemparse):
        eggflag = 0
        if(itemparse.lower() in chefnames):
            #eggflag 1 trying to cook chef
            eggflag = 1
            itemparse = self.nickcheck(ctx)
        return itemparse, eggflag

    def responsemenu(self, ctx, day, results , re):
        header, body, footer = '', '', ''
        dmheader, dmbody, dmfooter = '', '', ''
        #header
        if(re['newmenflag'] == 1):
           header = 'Created new menu! \n'
        #body
        if(results[1] == 0):
            body = 'You are preparing ' + results[0] + ' on ' + day + '!'
        elif(results[1] == 1):
            #eggflag 1 trying to cook chef
            dmbody = 'https://youtu.be/aPh2cu3vGCE?t=36'
            body = '<:sagioof:761617822588731414> <:sagioof:761617822588731414> <:sagioof:761617822588731414> <:sagioof:761617822588731414> \n' + results[0] + ', no we are not doing that. \n <:sagioof:761617822588731414> <:sagioof:761617822588731414> <:sagioof:761617822588731414> <:sagioof:761617822588731414> '
        #footer
        #composition
        directmessage = (dmheader + dmbody + dmfooter)
        message = (header + body + footer)
        return directmessage, message
    
    def updatefile(self, re):
        menufile = open(re['menpath'],'w')
        menufile.write(json.dumps(re['mendata']))
        menufile.close

    @commands.command(name='Menu', aliases=menualias)
    async def plan(self,ctx, *arg):
        '''Lists the current week menu Monday to Sunday'''
        re = self.chmen(ctx)
        currentday = datetime.date.today()
        year, week_num, day_of_week = currentday.isocalendar()
        menlist = '\n'
        if(re['newmenflag'] == 1):
            menlist = ('Created new menu! \n')
        for x in re['mendata']:
            menlist = menlist+f'{x.capitalize()}, {re["mendata"][x][0]} by {re["mendata"][x][1]} \n'
        await ctx.send(f"The menu for the {ordinal(week_num)} week this year is: \n" + menlist)


    @commands.command(name='Clear', aliases=destructionalias)
    async def clear(self, ctx, day):
        '''Use with a day or week after to clear the menu'''
        re = self.chmen(ctx)
        if(day.lower() in dowalias):
            re['mendata'][day.lower()][0] = 'None'
            re['mendata'][day.lower()][1] = 'None'
            self.updatefile(re)
            await ctx.send(day.capitalize() + ' has been cleared!')
        elif (day in weekalias):
            menufile = open(re['menpath'],'w')
            menufile.write(json.dumps(menweek))
            menufile.close
            await ctx.send('The entire week has been reset.')
        else:
            await ctx.send('That isn''t a day..')


    @commands.command(name='Give', aliases=assignmentalias)
    async def funcname(self, ctx, day, *newassign: str):
        '''Use Give and another '''
        re = self.chmen(ctx)
        newassigncon = ''
        for cats in newassign:
            newassigncon = newassigncon + ' ' + cats
        if(day in dowalias):
            re['mendata'][day.lower()][1] = newassigncon
        self.updatefile(re)
        await ctx.send(newassigncon.capitalize() + ' is now cooking on ' + day + '!')


    @commands.command(name = 'Monday',aliases=dowalias)
    async def monday(self, ctx, *itemraw: str,):
        '''Use any day of the week thent he food item to make a plan'''
        day = ctx.invoked_with
        who = self.nickcheck(ctx)
        re = self.chmen(ctx)
        itemparse = self.itemprep(itemraw)
        results = self.eggcheckmenu(ctx, itemparse)
        re['mendata'][day.lower()][0] = results[0]
        re['mendata'][day.lower()][1] = who
        self.updatefile(re)
        preppedmsg = self.responsemenu(ctx, day, results, re)
        if(preppedmsg[0] == ''):
            await ctx.send(preppedmsg[1])
        else:
            await ctx.author.send(preppedmsg[0])
            await ctx.send(preppedmsg[1])
            
def setup(bot):
    bot.add_cog(Menu_Management(bot))