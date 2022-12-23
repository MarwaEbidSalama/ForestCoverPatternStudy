# Forest Cover (FC) change in a small mountain range in the middle of Germany:

A case study of the thuringa/ franconian forest

General Plan of Action:

1. Choosing the right dataset (probably S2 data)
2. Choosing the region: here is a image of the region I have in my mind. I think we should start with a rectangle spanning from Naila to Eisenach.

| ![plot](./images/map1.png) | 
| ![plot](./images/map2.png)+ |
| --- | --- |

So, i think the ares we should look at are (odered by a somehow arbitrary hierarchy):

1. Frankenwald (franconian forest)
2. Thüringisches/Fränkisches Schiefergebirge (thuringia/ franconian slate mountains)
3. Thüringer Wald (thuringia forest)
4. Fichtelgebirge (fichtel mountains)

I would leave out the vogtland (i don't have to much of reason for it, but i don't think it's too much connect to the before mentioned). I included the fichtel mountains as they've seen quite some forest cover loss in the past 5 years too.

3. Mask the region for forest/urban area:

→ get the region of franconian forest

→ retrieve a filter function/ binary masked that is gridded over lat / lon

4. Time axis:

Main Problem: cloud cover → have to look for cloud free mosaics

Choose best pixel values for summer (something between JJAS), for

each year of the available years. Depending on the dataset we have to see what's possible

5. Variables:

We agreed that the NDVI will be our primary source for deriving the state of forest. We'll correlate the derived values with SPEI index and soil moisture.

| **Variable** | NDVI | SPEI | soil moisture |
| --- | --- | --- | --- |
| **use case** | state of trees, condition of trees | general enviromental condtions, measure for draught stress on trees | another way to look at the effective drought stress on the trees |
| **notes** |
 |
 |
 |

**Meeting 23.12.22 12:00**

-We agreed on a region. The shapefile will be uploaded to the repository (still in the making)

-Marwa will focus on the high level landuse products and already get us some metrics (percentage of forest cover change, etc.)

-Josh will automate a routine to get Sentinel-2 Level 2 data to extract RGB/ different bands (and maybe have expanded timeseries).

-