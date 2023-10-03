import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

def top_label(top, x_cord_2, y_cord_2, arrow, ax):
    
    """
    Given the position of the municipality, 
    the coordinates of the text, the shape of the arrow 
    and the figure, an annotation is added to the figure.

    Parameters
    ----------
    top : int [1,10]
    x_cord_2, y_cord_2 : float [e6]
    arrow : str
    ax : matplotlib.axes
    """
    
    global mapa_marg_top
    
    x_cord_1 = mapa_marg_top.centroid.x[top-1]
    y_cord_1 = mapa_marg_top.centroid.y[top-1]    
    
    name     = mapa_marg_top["NOM_MUN"].iloc[top-1] +", " + mapa_marg_top["Nombre de la entidad"].iloc[top-1]
    puesto   = mapa_marg_top["Lugar que ocupa en el contexto nacional"].iloc[top-1]
    text     = f" {puesto}: {name}"

    
    ax.annotate(
            text,
            xy     = (x_cord_1, y_cord_1), xycoords='data',
            xytext = (x_cord_2, y_cord_2), textcoords='data',
            size=14, va="center", ha="center",fontweight = "bold", fontname = "serif",
            arrowprops=dict(arrowstyle="->",connectionstyle=arrow))






#Urls
url_mapa_e = "/home/azael/Escritorio/mapa_marginacion/data/Marco geoestadístico 2010/mge2010v5_0.zip"
url_mapa_m = "/home/azael/Escritorio/mapa_marginacion/data/Marco geoestadístico 2010/mgm2010v5_0.zip"
url_marg   = "/home/azael/Escritorio/mapa_marginacion/data/IMM_2020.xls"

#Reading files
mapa_e     = gpd.read_file(url_mapa_e)
mapa_m     = gpd.read_file(url_mapa_m)
marg       = pd.read_excel(url_marg, skiprows = 3)


# Cleaning and preparation
marg       = marg.dropna(axis=0)
marg       = marg.set_index("Clave del municipio")
marg_norm  = marg.get(
    ["Nombre de la entidad",
    "Índice de marginación normalizado, 2020",
    "Lugar que ocupa en el contexto nacional"]
)
mapa_e["boundary"]= mapa_e.boundary
mapa_e            = mapa_e.set_geometry("boundary")
mapa_m["CVE"]     = mapa_m.CVE_ENT.str.cat(mapa_m.CVE_MUN)

    #Merge
mapa_marg = pd.merge(mapa_m, marg_norm, left_on="CVE", right_on="Clave del municipio")

    #Top municipalities
mapa_marg_top  = mapa_marg.sort_values("Lugar que ocupa en el contexto nacional").iloc[0:10]
mapa_marg_top["centroide"] = mapa_marg_top.centroid
mapa_marg_top = mapa_marg_top.set_geometry("centroide").reset_index()


#Ploting
fig, ax = plt.subplots()
fig.set_size_inches(15,15)
ax.set_title('Índice de marginación normalizado por municipio, 2020', 
             fontsize=16, 
             fontweight='bold',
             fontname = "serif")
ax.set_ylim(0, 2.5e6)
ax.set_xlim(0.5e6, 4.5e6)



    # ploting municipalities
mapa_marg.plot(
    column     = "Índice de marginación normalizado, 2020",
    cmap       = "bwr_r",
    scheme     = "QUANTILES",
    k          = 3,
    legend     = True,
    ax         = ax,
    zorder     = 1
)

    # ploting states's boundary
mapa_e.plot(
    color      = "k",
    ax         = ax,
    zorder     = 2
)

    # Ploting top
mapa_marg_top.plot(
    color      = "k",
    markersize = 50, 
    ax         = ax,
    zorder     = 3
)




top_label(1, 1.2e6, 1.1e6, "angle, angleA=90,angleB=0,rad=0.0", ax)
top_label(2, 1.3e6, 0.9e6, "bar, angle=0,fraction=-0.12", ax)
top_label(3, 1.4e6, 0.7e6, "bar, angle=0,fraction=-0.12", ax)
top_label(4, 1.5e6, 0.5e6, "bar, angle=0,fraction=-0.12", ax)
top_label(5, 1.9e6, 0.3e6, "angle, angleA=180,angleB=-90,rad=0.0", ax)
top_label(6, 3.8e6, 0.2e6, "angle, angleA=90,angleB=0,rad=0.0", ax)
top_label(7, 3.2e6, 2e6, "angle, angleA=1800,angleB=-90,rad=0.0", ax)
top_label(8, 3.4e6, 1.8e6, "angle, angleA=90,angleB=0,rad=0.0", ax)
top_label(9, 3.6e6, 1.6e6, "angle, angleA=-90,angleB=0,rad=0.0", ax)
top_label(10, 3.8e6, 1.4e6, "bar, fraction=-0.3,angle=180", ax)

fig.savefig("marginalization_map.jpeg")
fig.savefig("marginalization_map.svg")






