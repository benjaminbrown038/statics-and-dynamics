"""Regenerate the baseline free-body diagrams (requires Matplotlib)."""
from pathlib import Path
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Arc

root=Path(__file__).resolve().parents[1]
out=root/'docs/images'
out.mkdir(exist_ok=True)
navy='#153c5b'; blue='#1a79ad'; orange='#bd501f'; gray='#536674'

def arrow(ax,start,end,color=blue,lw=2):
    ax.annotate('',xy=end,xytext=start,arrowprops=dict(arrowstyle='-|>',color=color,lw=lw,mutation_scale=15))

fig,ax=plt.subplots(figsize=(9,4.5),layout='constrained')
ax.plot([0,1],[0,0],color=navy,lw=6,solid_capstyle='round')
ax.add_patch(Polygon([(0,-0.025),(-0.025,-0.10),(0.025,-0.10)],closed=True,fill=False,color=gray,lw=1.5))
ax.add_patch(Polygon([(1,-0.025),(.975,-0.085),(1.025,-0.085)],closed=True,fill=False,color=gray,lw=1.5))
for x in (.987,1.013): ax.add_patch(Circle((x,-.105),.01,fill=False,color=gray))
for i in range(1,10): arrow(ax,(i/10,.24),(i/10,.025),blue,1.4)
ax.plot([0,1],[.24,.24],color=blue,lw=1.2)
ax.text(.72,.29,'q = 200 N/m',color=blue,ha='center',fontsize=12)
arrow(ax,(.4,.55),(.4,.025),orange,2.4)
ax.text(.4,.59,'P = 1000 N',ha='center',color=orange,fontsize=12)
arrow(ax,(0,-.32),(0,.005))
arrow(ax,(1,-.32),(1,.005))
ax.text(0,-.38,'RA = 700 N',ha='center',color=blue,fontsize=11)
ax.text(1,-.38,'RB = 500 N',ha='center',color=blue,fontsize=11)
ax.text(.04,-.15,'A: pin',color=gray,fontsize=11)
ax.text(.88,-.16,'B: roller',color=gray,fontsize=11)
ax.annotate('',xy=(1,-.51),xytext=(0,-.51),arrowprops=dict(arrowstyle='<->',color=gray))
ax.text(.5,-.56,'L = 1 m; point load at x = 0.4 m',ha='center',va='top',fontsize=11,color=gray)
ax.set(xlim=(-.19,1.19),ylim=(-.69,.73),title='Tier 1 · Supported beam free-body diagram')
ax.axis('off')
fig.savefig(out/'beam_fbd.png',dpi=160)
plt.close(fig)

fig,ax=plt.subplots(figsize=(8,6),layout='constrained')
theta=math.radians(45)
A=(-.1,.08); B=(.06*math.cos(theta),.06*math.sin(theta)); tip=(.3*math.cos(theta),.3*math.sin(theta)); center=(tip[0]/2,tip[1]/2)
ax.plot([0,tip[0]],[0,tip[1]],color=navy,lw=8,solid_capstyle='round')
ax.plot([A[0],B[0]],[A[1],B[1]],ls='--',color=gray,lw=2)
ax.scatter([A[0],B[0],tip[0]],[A[1],B[1],tip[1]],color=[gray,navy,orange],s=[70,35,85],zorder=4)
ax.add_patch(Circle((0,0),.007,fc='white',ec=navy,lw=2,zorder=5))
length=math.hypot(A[0]-B[0],A[1]-B[1]); u=((A[0]-B[0])/length,(A[1]-B[1])/length)
arrow(ax,B,(B[0]+.07*u[0],B[1]+.07*u[1]),blue)
ax.text(-.015,.087,'F toward A',color=blue,fontsize=11)
arrow(ax,(0,0),(.066,0)); ax.text(.055,-.02,'Rx',color=blue,fontsize=11)
arrow(ax,(0,0),(0,.065)); ax.text(-.02,.035,'Ry',color=blue,fontsize=11)
arrow(ax,center,(center[0],center[1]-.073),orange)
ax.text(center[0]+.008,center[1]-.055,'mr g',color=orange,fontsize=11)
arrow(ax,tip,(tip[0],tip[1]-.08),orange)
ax.text(tip[0]+.01,tip[1]-.05,'mp g',color=orange,fontsize=11)
ax.text(A[0]-.008,A[1]+.018,'A: fixed anchor',color=gray,fontsize=11,ha='left')
ax.text(B[0]+.012,B[1]-.012,'B',fontsize=11,color=navy)
ax.text(-.03,-.025,'O: pivot',fontsize=11,color=navy,ha='right')
ax.text(.13,.16,'Rigid arm',rotation=45,fontsize=12,color=navy)
ax.add_patch(Arc((0,0),.15,.15,theta1=0,theta2=45,color=gray,lw=1))
ax.text(.075,.021,'θ',fontsize=13,color=gray)
ax.set(xlim=(-.19,.30),ylim=(-.055,.285),aspect='equal',title='Tier 7 · Forces on the moving arm (shown at 45°)')
ax.axis('off')
fig.savefig(out/'arm_fbd.png',dpi=160)
plt.close(fig)
print('Created beam and actuator-arm free-body diagrams.')
