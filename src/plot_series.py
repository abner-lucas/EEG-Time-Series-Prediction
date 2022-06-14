import pandas as pd
import random
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from plotly.offline import init_notebook_mode, iplot

class PlotSeries:
    def __init__(self):
        pass

    def plot_3dSurface_and_heatmap(df, stimulus=None):
        init_notebook_mode(connected=True) ## plotly iniciando
        seed = 123
        random.seed = seed

        sensor_positions = df[['sensor_position', 'channel']].drop_duplicates().reset_index(drop=True).drop(['channel'], axis=1).reset_index(drop=False).rename(columns={'index':'channel'})['sensor_position']
        channels = df[['sensor_position', 'channel']].drop_duplicates().reset_index(drop=True).drop(['channel'], axis=1).reset_index(drop=False).rename(columns={'index':'channel'})['channel']

        data = df[['channel', 'sample_num', 'sensor_value']]
        temp_df = pd.pivot_table(data, values='sensor_value', index='channel', columns='sample_num', aggfunc='mean').values.tolist()
        data = [go.Surface(z=temp_df, colorscale='Bluered')]
        if stimulus == None:
            stimulus = df['condition'].unique()[0]
        group = df['group'].unique()[0]
        subject_id = df['subject_id'].unique()[0]
        layout = go.Layout(
            title='<br>3d Surface and Heatmap of Sensor Values for '+' Subject '+ subject_id +' and '+ stimulus + ' Stimulus for ' + group + ' Group',
            width=1000,
            height=600,
            autosize=False,
            margin=dict(t=0, b=0, l=0, r=0),
            scene=dict(
                xaxis=dict(
                    title='Time (sample number / ms)',
                    gridcolor='rgb(255, 255, 255)',
        #            erolinecolor='rgb(255, 255, 255)',
                    showbackground=True,
                    backgroundcolor='rgb(230, 230,230)'
                ),
                yaxis=dict(
                    title='Channel',
                    tickvals=channels,
                    ticktext=sensor_positions,
                    gridcolor='rgb(255, 255, 255)',
                    zerolinecolor='rgb(255, 255, 255)',
                    showbackground=True,
                    backgroundcolor='rgb(230, 230, 230)'
                ),
                zaxis=dict(
                    title='Sensor Value (µV)',
                    gridcolor='rgb(255, 255, 255)',
                    zerolinecolor='rgb(255, 255, 255)',
                    showbackground=True,
                    backgroundcolor='rgb(230, 230,230)'
                ),
                aspectratio = dict(x=1, y=1, z=0.5),
                aspectmode = 'manual'
            )
        )

        updatemenus=list([
            dict(
                buttons=list([   
                    dict(
                        args=['type', 'surface'],
                        label='3D Surface',
                        method='restyle'
                    ),
                    dict(
                        args=['type', 'heatmap'],
                        label='Heatmap',
                        method='restyle'
                    )             
                ]),
                direction = 'left',
                pad = {'r': 10, 't': 10},
                showactive = True,
                type = 'buttons',
                x = -0.1,
                xanchor = 'left',
                y = 1.1,
                yanchor = 'top' 
            ),
        ])

        annotations = list([
            dict(text='Trace type:', x=0, y=1.085, yref='paper', align='left', showarrow=False)
        ])
        layout['updatemenus'] = updatemenus
        layout['annotations'] = annotations

        fig = dict(data=data, layout=layout)
        iplot(fig)

    def plot_2D(raw_data, title=None):
        x = raw_data.index.values
        fig = plt.figure(figsize=(20,6))
        for i in range(len(raw_data.columns)):
            plt.plot(x, raw_data[raw_data.columns[i]], label=raw_data.columns[i])
        plt.legend()
        if title == None:
            plt.title("Plot Multiple channels",fontsize=15)
        else:
            plt.title(f"Plot Multiple channels - {title}",fontsize=15)
        plt.xlabel("Time (ms)",fontsize=13)
        plt.ylabel("Value (µV)",fontsize=13)
        plt.show()
        return fig

class Subplot2D:
  def __init__(self, nrows, ncols):
    self.fig = plt.figure(figsize=(18,14))
    self.nrows = nrows
    self.ncols = ncols
    self.axes = []

  def add_subplot(self, raw_data, index, title, sharex=None, kind='line'):
    x = raw_data.index.values
    if sharex is None:
      ax = plt.subplot(self.nrows, self.ncols, index)
    else:
      ax = plt.subplot(self.nrows, self.ncols, index, sharex=self.axes[sharex-1])
    for i in range(len(raw_data.columns)):
        if kind == 'bar':
            ax.bar(x, raw_data[raw_data.columns[i]], label=raw_data.columns[i])
        else:
            ax.plot(x, raw_data[raw_data.columns[i]], label=raw_data.columns[i])
    ax.legend()
    ax.set_title(title, fontsize=15)
    ax.set_xlabel("Time (ms)",fontsize=13)
    ax.set_ylabel("Value (µV)",fontsize=13)
    self.axes.append(ax)

  def show(self):
    plt.tight_layout()
    plt.show()
    return self.fig