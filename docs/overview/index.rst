################
Openads Overview
################

The open ads system is an open source rotational ad system. This means that the ad system randomly chooses
unique advertisements to display so that the same ad will not display twice in the same page retrieval.

System overview
---------------

The system is based off two administration sections. The first is the admin section which is not available
to the providers. This is where adverts are created, edited and deleted. In the admin section, there are two
main subsections. 

#. The first is the provider edit view, where providers are created and edited. Each advert will have a
   provider associated with it for the later statistics section of the site. Providers can also have an
   assigned user, which will have some edit ability and is able to view the statistics of all that providers
   ads.
#. The second is the advertisement section, where advertisements are created and edited. Each advertisement
   will have the following properties

   #. **The type of advertisement**: The type of advertisement can be either a banner ad or a side ad. The
      banner ad is the wider ad that is shown individually, whereas the side ad is the small ad that is shown
      along side 3 other ads.
   #. **The provider**: The provider that the ad belongs to.
   #. **An image**: The image to be displayed in the rotation.
   #. **The URL**: The link that the ad points to.
   #. **The status**: The status of the ad. It can be one of three types:

      #. **Active**: Active ads are ads that are in the rotation.
      #. **Inactive**: Inactive ads are ads that are not in the rotation.
      #. **Pending**: Pending ads are ads that have been submitted by the providers, but need to be authorized
         by an admin before it enters the rotation.

