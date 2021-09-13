import streamlit as st
from bson.son import SON
from pymongo import MongoClient
import pandas as pd
import plotly_express as px
from PIL import Image
client = MongoClient("mongodb+srv://srip_92:FvvhmRfxHBZDqzJO@cluster0.k7ocd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
database = client["Cluster0"]
collection = database["roadInjury"]
collection2 = database["transport"]



st.markdown(
        f"""
<style>
    .reportview-container .main .block-container{{
        max-width: 90%;
        padding-top: 5rem;
        padding-right: 5rem;
        padding-left: 5rem;
        padding-bottom: 5rem;
    }}
    img{{
    	max-width:40%;
    	margin-bottom:40px;
    }}
</style>
""",
        unsafe_allow_html=True,
    )
header_container = st.container()
stats_container = st.container()
with header_container:
    Logoimage = Image.open(r"E:\Shripad_Den\SRH\Master thesis\Proposal\Images\Srh_Logo.png")
    st.image(Logoimage)
    st.title("Information Systems Project")
    st.header("Welcome to the Smart Mobility User Stories!!!")
    st.subheader("Use case 1")
st.write("To analyse the number of private vehicles used vs public transport")
pipeline = [
    {
        u"$match": {
            u"mode": {
                u"$in": [
                    u"CAR",
                    u"CARPOOL",
                    u"PUBLICTR"
                ]
            },
            u"reportyear": {
                u"$in": [
                    2016,
                    2017,
                    2018,
                    2019,
                    2020
                ]
            }
        }
    },
    {
        u"$group": {
            u"_id": {
                u"mode": u"$mode",
                u"reportyear": u"$reportyear"
            },
            u"AVG(percent)": {
                u"$avg": u"$percent"
            }
        }
    },
    {
        u"$project": {
            u"AVG(percent)": u"$AVG(percent)",
            u"mode": u"$_id.mode",
            u"reportyear": u"$_id.reportyear",
            u"_id": 0
        }
    },
    {
        u"$sort": SON([ (u"reportyear", 1), (u"AVG(percent)", -1) ])
    }
]

cursor = collection2.aggregate(
    pipeline,
    allowDiskUse = True
)
try:
    result_dict0 = []
    for i in cursor:
        result_dict0.append(i)

finally:
    client.close()
vis_df = pd.DataFrame.from_dict(result_dict0)

fig1 = px.bar(vis_df,x='reportyear',y='AVG(percent)',color='mode',barmode='group')

fig1.update_layout(showlegend=False,
		width=400,
		height=400,
		margin=dict(l=1,r=1,b=1,t=1),
		font=dict(color='#383635', size=15))

st.write(fig1)


st.subheader("Use case 2")
st.write("To analyse the figures of all ethnic groups using different modes of transportation")
pipeline = [
    {
        u"$group": {
            u"_id": {
                u"race_eth_name": u"$race_eth_name",
                u"mode": u"$mode"
            },
            u"AVG(percent)": {
                u"$avg": u"$percent"
            }
        }
    },
    {
        u"$project": {
            u"AVG(percent)": u"$AVG(percent)",
            u"race_eth_name": u"$_id.race_eth_name",
            u"mode": u"$_id.mode",
            u"_id": 0
        }
    },
    {
        u"$sort": SON([ (u"AVG(percent)", -1) ])
    }
]

cursor = collection2.aggregate(
    pipeline,
    allowDiskUse = True
)
try:
    result_dict1 = []
    for i in cursor:
        result_dict1.append(i)
finally:
    client.close()
vis_df1 = pd.DataFrame.from_dict(result_dict1)


fig2 = px.bar(vis_df1,x='race_eth_name',y='AVG(percent)',color='mode',barmode='group')
st.write(fig2)

st.subheader("Use case 3")
st.write("To analyse the accidents caused by different modes of transportation over the past decade")
pipeline = [
    {
        u"$group": {
            u"_id": {
                u"mode": u"$mode",
                u"reportyear": u"$reportyear"
            },
            u"SUM(injuries)": {
                u"$sum": u"$injuries"
            }
        }
    },
    {
        u"$project": {
            u"SUM(injuries)": u"$SUM(injuries)",
            u"mode": u"$_id.mode",
            u"reportyear": u"$_id.reportyear",
            u"_id": 0
        }
    },
    {
        u"$sort": SON([ (u"mode", 1),(u"reportyear", 1) ])
    }
]

cursor = collection.aggregate(
    pipeline,
    allowDiskUse = True
)
try:
    result_dict2 = []
    for i in cursor:
        result_dict2.append(i)


finally:
    client.close()

vis_df2 = pd.DataFrame.from_dict(result_dict2)


fig3 = px.line(vis_df2,x='reportyear',y='SUM(injuries)',color='mode')

st.write(fig3)



st.subheader("Use case 4")
st.write("To analyse the trend of bicyclists and pedestrians over the years")

pipeline = [
    {
        u"$match": {
            u"mode": {
                u"$in": [
                    u"WALK",
                    u"BICYCLE"
                ]
            }
        }
    },
    {
        u"$group": {
            u"_id": {
                u"mode": u"$mode",
                u"reportyear": u"$reportyear"
            },
            u"SUM(pop_mode)": {
                u"$sum": u"$pop_mode"
            }
        }
    },
    {
        u"$project": {
            u"SUM(pop_mode)": u"$SUM(pop_mode)",
            u"mode": u"$_id.mode",
            u"reportyear": u"$_id.reportyear",
            u"_id": 0
        }
    },
    {
        u"$sort": SON([ (u"reportyear", 1) ])
    }
]

cursor = collection2.aggregate(
    pipeline,
    allowDiskUse = True
)
try:
    result_dict3 = []

    for i in cursor:
        result_dict3.append(i)
finally:
    client.close()
vis_df3 = pd.DataFrame.from_dict(result_dict3)
#print(vis_df3)
fig4 = px.bar(vis_df3, x="reportyear", y="SUM(pop_mode)", color="mode")

st.write(fig4)

st.subheader("Use case 5")
st.write("To analyse the trend in various kinds of accidents happened in the California County")
pipeline = [
    {
        u"$match": {
            u"county_name": u"California",
            u"reportyear": {
                u"$in": [
                    2016,
                    2017,
                    2018,
                    2019,
                    2020
                ]
            }
        }
    },
    {
        u"$group": {
            u"_id": {
                u"mode": u"$mode",
                u"county_name": u"$county_name",
                u"reportyear": u"$reportyear"
            },
            u"SUM(injuries)": {
                u"$sum": u"$injuries"
            }
        }
    },
    {
        u"$project": {
            u"mode": u"$_id.mode",
            u"reportyear": u"$_id.reportyear",
            u"SUM(injuries)": u"$SUM(injuries)",
            u"county_name": u"$_id.county_name",
            u"_id": 0
        }
    },
    {
        u"$sort": SON([ (u"mode", 1), (u"reportyear", -1), (u"SUM(injuries)", -1) ])
    }
]

cursor = collection.aggregate(
    pipeline,
    allowDiskUse = True
)
try:

    result_dict4 = []
    for i in cursor:
        result_dict4.append(i)
finally:
    client.close()
vis_df4 = pd.DataFrame.from_dict(result_dict4)
fig5 = px.bar(vis_df4, x="reportyear", y="SUM(injuries)", color="mode",barmode="group")
st.write(fig5)

st.subheader("Use case 6")
st.write("To analyse the figures of injuries and the severity")
pipeline = [
    {
        u"$group": {
            u"_id": {
                u"mode": u"$mode",
                u"severity": u"$severity"
            },
            u"SUM(injuries)": {
                u"$sum": u"$injuries"
            }
        }
    },
    {
        u"$project": {
            u"SUM(injuries)": u"$SUM(injuries)",
            u"severity": u"$_id.severity",
            u"mode": u"$_id.mode",
            u"_id": 0
        }
    },
    {
        u"$sort": SON([ (u"severity", 1), (u"mode", 1) ])
    }
]

cursor = collection.aggregate(
    pipeline,
    allowDiskUse = True
)
try:
    result_dict5 = []
    for i in cursor:
        result_dict5.append(i)

finally:
    client.close()
visdf5 = pd.DataFrame.from_dict(result_dict5)

fig6 = px.bar(visdf5,x="mode",y="SUM(injuries)",color="severity",barmode="group")
st.write(fig6)


st.subheader("Use case 7")
st.write("To analyse the areas with highest accidents based on mode of accident")
pipeline = [
    {
        u"$group": {
            u"_id": {
                u"mode": u"$mode",
                u"county_name": u"$county_name"
            },
            u"SUM(injuries)": {
                u"$sum": u"$injuries"
            }
        }
    },
    {
        u"$project": {
            u"SUM(injuries)": u"$SUM(injuries)",
            u"county_name": u"$_id.county_name",
            u"mode": u"$_id.mode",
            u"_id": 0
        }
    },
    {
        u"$sort": SON([ (u"SUM(injuries)", -1) ])
    }
]

cursor = collection.aggregate(
    pipeline,
    allowDiskUse = True
)
try:
    result_dict6 = []
    for i in cursor:
        result_dict6.append(i)
finally:
    client.close()

visdf6=pd.DataFrame.from_dict(result_dict6)

#print(visdf)
filter_li=["California","Los Angeles","San Bernardino"]
vvisdf = visdf6.query("county_name== @filter_li")
fig7 = px.bar(vvisdf,x="county_name",y="SUM(injuries)",color="mode",barmode="group")
st.write(fig7)


