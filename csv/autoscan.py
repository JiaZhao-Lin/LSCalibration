#%%
## Import

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



# %%
## Data Processing

df_Sep = pd.read_csv('inFiles/2023-09.csv')
df_Sep['datetime_format'] = df_Sep['datetime'].apply(lambda x: x.split('.')[0].replace(' ', '|'))
df_Sep_LSC_x = df_Sep.loc[df_Sep['Scan_Name'] == 'LSC_x_2x9st_30s_moveSep.txt']
df_Sep_LSC_y = df_Sep.loc[df_Sep['Scan_Name'] == 'LSC_y_2x9st_30s_moveSep.txt']
df_Sep_LSC_x_y = pd.concat([df_Sep_LSC_x, df_Sep_LSC_y], axis=0)

df_Oct = pd.read_csv('infiles/2023-10.csv')
df_Oct['datetime_format'] = df_Oct['datetime'].apply(lambda x: x.split('.')[0].replace(' ', '|'))
df_Oct_LSC_x = df_Oct.loc[df_Oct['Scan_Name'] == 'LSC_x_2x9st_30s_moveOct.txt']
df_Oct_LSC_y = df_Oct.loc[df_Oct['Scan_Name'] == 'LSC_y_2x9st_30s_moveOct.txt']



# %%
## Data Visualization

'''
xingplane is the horizontal LHC plane (synonyms: XZ plane, X-plane, crossing plane
sepPlane is the vertical LHC plane (synonyms: YZ plane, Y plane, separation plane)
In LumiScanStatus: 
STANDBY in the beginning and in the end of scans
ACQUIRING were data-taking is performed
IDLE, TRIMMING - between steps.
In practice, can remove first and last seconds because there is the overlap with no-data-taking but may be it is too strict. 
'''

print(df_Sep_LSC_x.describe())
df_Sep_LSC_x.head()

# df_Sep_LSC_x.columns

# df_Sep['Scan_Name'].unique()
# df_Oct['Scan_Name'].unique()

# df_Sep_LSC_y.describe()
# df_Sep_LSC_y.head()

# df_Oct_LSC_x.describe()
# df_Oct_LSC_x.head()

# df_Oct_LSC_y.describe()
# df_Oct_LSC_y.head()



# %%
## Step

df_Sep_LSC_x_acq = df_Sep_LSC_x.loc[df_Sep_LSC_x['LumiScan_Status'] == 'ACQUIRING']

df_Sep_LSC_x_acq.plot(
				# figsize=(16, 8),
				x='timestamp', 
				y=[
					# 'Read_Nominal_Displacement_B1_xingPlane', 
		 			# 'Read_Nominal_Displacement_B2_xingPlane',
					'Set_Nominal_Displacement_B1_xingPlane',
					'Set_Nominal_Displacement_B2_xingPlane'	
				], 
				style='.',
				title='LSC_x_2x9st_30s_moveSep: ACQUIRING'
				  )
df_Sep_LSC_x_acq.plot(
				# figsize=(4, 3),
				x='timestamp', 
				y=[
					# 'Read_Nominal_Displacement_B1_sepPlane',
					# 'Read_Nominal_Displacement_B2_sepPlane',
					'Set_Nominal_Displacement_B1_sepPlane',
					'Set_Nominal_Displacement_B2_sepPlane',
				], 
				style='.',
				title='LSC_x_2x9st_30s_moveSep: ACQUIRING'
				  )

# df_Sep_LSC_x_acq.plot(
# 				# figsize=(4, 3),
# 				x='timestamp', 
# 				y='Nominal_Separation_Plane', 
# 				style='.',
# 				title='LSC_x_2x9st_30s_moveSep: ACQUIRING'
# 				  )


df_Sep_LSC_y_acq = df_Sep_LSC_y.loc[df_Sep_LSC_y['LumiScan_Status'] == 'ACQUIRING']

df_Sep_LSC_y_acq.plot(
				# figsize=(12, 8),
				x='timestamp', 
				y=[
					# 'Read_Nominal_Displacement_B1_xingPlane', 
		 			# 'Read_Nominal_Displacement_B2_xingPlane',
					'Set_Nominal_Displacement_B1_xingPlane',
					'Set_Nominal_Displacement_B2_xingPlane'	
				], 
				style='.',
				title='LSC_y_2x9st_30s_moveSep: ACQUIRING'
				  )
df_Sep_LSC_y_acq.plot(
				# figsize=(4, 3),
				x='timestamp', 
				y=[
					# 'Read_Nominal_Displacement_B1_sepPlane',
					# 'Read_Nominal_Displacement_B2_sepPlane',
					'Set_Nominal_Displacement_B1_sepPlane',
					'Set_Nominal_Displacement_B2_sepPlane',
				], 
				style='.',
				title='LSC_y_2x9st_30s_moveSep: ACQUIRING'
				  )



# %%
## Processing
'''
In my practice, may removed first and last seconds because there is the overlap with no-data-taking but may be it is too strict. 
'''
pd.set_option('display.float_format', '{:}'.format)
# pd.set_option('display.float_format', '{:.2f}'.format)

df_Sep_LSC_x_acq_step = df_Sep_LSC_x_acq.groupby('Step')
df_Sep_LSC_y_acq_step = df_Sep_LSC_y_acq.groupby('Step')

#= select the group with the Step_Progress with the maximum value and the minimum value are 30 and 0, respectively
filter_0Start = df_Sep_LSC_x_acq_step['Step_Progress'].agg('min') == 0
filter_30End = df_Sep_LSC_x_acq_step['Step_Progress'].agg('max') == 30

data_table = ['datetime_format', 'timestamp', 'Step_Progress',
			  'Set_Nominal_Displacement_B1_xingPlane', 'Set_Nominal_Displacement_B2_xingPlane',
			  'Set_Nominal_Displacement_B1_sepPlane', 'Set_Nominal_Displacement_B2_sepPlane',
			  'Nominal_Separation',
				]

df_Sep_LSC_x_acq_step_selected = df_Sep_LSC_x_acq_step[data_table].agg(['min', 'max']).loc[filter_0Start].loc[filter_30End]
df_Sep_LSC_y_acq_step_selected = df_Sep_LSC_y_acq_step[data_table].agg(['min', 'max']).loc[filter_0Start].loc[filter_30End]

def get_df_selected(df):
	df_out = pd.DataFrame()
	df_out['datetime_start'] = df['datetime_format']['min'].values
	df_out['datetime_end'] = df['datetime_format']['max'].values
	df_out['timestamp_start'] = df['timestamp']['min'].values
	df_out['timestamp_end'] = df['timestamp']['max'].values
	df_out['Set_Nominal_Displacement_B1_xingPlane'] = df['Set_Nominal_Displacement_B1_xingPlane']['min'].values
	df_out['Set_Nominal_Displacement_B2_xingPlane'] = df['Set_Nominal_Displacement_B2_xingPlane']['min'].values
	df_out['Set_Nominal_Displacement_B1_sepPlane'] = df['Set_Nominal_Displacement_B1_sepPlane']['min'].values
	df_out['Set_Nominal_Displacement_B2_sepPlane'] = df['Set_Nominal_Displacement_B2_sepPlane']['min'].values
	df_out['Nominal_Separation'] = df['Nominal_Separation']['min'].values

	return df_out

df_x_out = get_df_selected(df_Sep_LSC_x_acq_step_selected)
df_y_out = get_df_selected(df_Sep_LSC_y_acq_step_selected)

print(df_x_out)
print(df_y_out)

df_x_out.to_csv('outFiles/df_x_Sep_LSC_x_acq_selected.csv', index=False)
df_y_out.to_csv('outFiles/df_y_Sep_LSC_y_acq_selected.csv', index=False)



#%%
## Plot

df_x_out.plot(
				# figsize=(16, 8),
				x='timestamp_start',
				y=[
					'Set_Nominal_Displacement_B1_xingPlane', 
					'Set_Nominal_Displacement_B2_xingPlane',
					# 'Nominal_Separation'
				], 
				style='.',
				title='LSC_x_2x9st_30s_moveSep: ACQUIRING'
				  )
