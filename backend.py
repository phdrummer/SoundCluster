#!/usr/bin/env python3
from termcolor import colored
from pymongo import MongoClient
from tabulate import tabulate
import os
import soundcloud
import getpass
import pdb


#scClient= soundcloud.Client(client_id='8e906fb7c324fc6640fd3fc08ef9d1ff',client_secret='acd3a93bdfcf1dd65ed33497f091800', redirect_uri= url_for('logged_in'))
#redirect client.authorize_url()

# Initializes Mongo
mongoClient = MongoClient()
db = mongoClient.followings

def main():
    # Clear the screen
    os.system('cls' if os.name == 'nt' else 'clear')



    # Welcome Message
    print(colored("####################", "cyan"))
    print(colored("SoundCluster, v 0.1","cyan")) 
    print(colored("Made by Phil Leonowens","cyan")) 
    print(colored("####################", "cyan"))
    # 

    scUsername = input(colored("Soundcloud Username:", "blue"))
    scPass = getpass.getpass(colored("Password:","blue"))

    command = "f" 
    try:
        scClient = soundcloud.Client(
            client_id='8e906fb7c324fc6640fd3fc08ef9d1ff',
            client_secret='aacd3a93bdfcf1dd65ed33497f091800',
            username=scUsername,
            password=scPass
    )
        print(colored(scClient.get('/me').username, 'red'),'is logged in')
        print( "1) Acquire Followings")
        print( "2) Print Followings ")
    except:
        print(colored("Incorrect Login", "white","on_red"))
        command="q"
    while command != "q":
        command = input("Enter Command:")
        if command == "1":
            updateFollowings(scClient)

        if command == "2":
            printFollowings(scClient)


def printFollowings(client):
    print('You are following', colored( client.get('/me').followings_count,'green'),'users')
    followings = db.followings.find()
    table = [[follower['username'],  follower['city'], follower['followers_count']]   for follower in followings]
    headers=["Username", "Location", "Followers"]
    print(tabulate(table, headers, tablefmt="fancy_grid"))


def updateLikes(client):
    totalFollowers = list()
    # start paging through results, 200 at a time
    followers = client.get('/me/followings', limit=200,
                        linked_partitioning=1)
    totalFollowers = totalFollowers + [follower for follower in (followers.collection)]
    previousResult = followers

    # if there are more than 200 followers, keeps getting them
    while hasattr(previousResult,'next_href'):
        followers = client.get(previousResult.next_href, limit=200,linked_partitioning=1) 
        totalFollowers = totalFollowers + list(followers.collection)
        previousResult = followers
    db.followings.insert_many(totalFollowers)

def updateFollowings(client):
    totalFollowers = list()
    # start paging through results, 200 at a time
    followers = client.get('/me/followings', limit=200,
                        linked_partitioning=1)
    totalFollowers = totalFollowers + [follower for follower in (followers.collection)]
    previousResult = followers

    # if there are more than 200 followers, keeps getting them
    while hasattr(previousResult,'next_href'):
        followers = client.get(previousResult.next_href, limit=200,linked_partitioning=1) 
        totalFollowers = totalFollowers + list(followers.collection)
        previousResult = followers
    db.followings.insert_many(totalFollowers)


if __name__ == '__main__':
    main()
