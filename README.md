# Open Advertisements

[![Build Status](https://travis-ci.org/OpenAds/OpenAds.png?branch=feature/user_statistics)](https://travis-ci.org/OpenAds/OpenAds)

An open source rotating advert system, specifically aimed ads related to hosting services. 
It uses a rotational system where no two ads are shown together but also fails gracefully if
there are not enough ads to be displayed.

It features two types of ads:

* Top ads (728 x 90)
* Sidebar ads (125 x 125)

The sidebar ads are grouped in 4 in the following format:

    [Advertisement] [Advertisement] 
    [Advertisement] [Advertisement] 

The group width total is 245px since there is a 4px margin inbetween the ads.

