# First Epoch (Done) 

* starting 2020, November 21st and November 22nd
* finished 2020, December 20th

As of 2020, december 20th speaking, 

The first epoch contained a lot of groundwork for the UI and the backend involving the basic data
structures. Like create and edit decision models; create and edit decision nodes; create and edit
decision node transitions; create and edit knowledge base articles. UI-wise as well as backend wise.   

For the very first iterations I simply used some hashmaps and hard coded values, to make the UI 
work as early as possible. At the end of the first epoch I started to implement more and more
of the persistence of the current state, and load the persisted information; Of the models, threads, 
articles and so on.

The current state is, that the UI can present list of models, threads and articles, has many dialogs
to edit the model. And the final step was to allow to view the model to be exported as a xgml file
which can be edited via YED. The layouting in the export is poor but can be rearranged by using the
YED itself. Therefore i can skip a routing and layouting mechanism and focus on other things.

Also one of the major achievements in the first epoch is the groundwork for the DecisionExecutionEngine
which is basically the core of the whole project, or the reason why this project exists. This engine
will execute a graph. This graph should be able to edit, so the Editor came even before the engine was
ready. As of the engine speaking, it is not ready yet, since it can't execute the decision node
evaluation functions / signatures nor the decision node transition functions yet.

# Second Epoch (Done)

* starting 2020, December 21st
* finished 2020, December 27th

As of 2020, december 26th speaking, 

The second epochs goal was to create a ThreadReportGenerator, which basically summarizes and collects 
what decision were made during processing the decision process. The main objective was to create the
report "make it work" from whichever data is available, if it wasn't it was added to the project on 
the backend side. I added a execution log as well as a "parser" for the execution log.

The whole system now supports a decision thread environmnent which is referenced from the decision 
thread. The decision thread environment is generated on start, and transitions between decision nodes 
are logged into the thread environment.  

Why does this matter? The main goal is to automatically create a report at the end of the execution
of the decision tree. 

So basically the idea was also to make the ThreadReportGenerator work, with as little effort as possible,
and evolve the current code base to meet these new requirements. I archived all current requirements
and decided for most of them to implement them later or never.

Also one major concern was the integration of the knowledge base into the modelling of the decision 
nodes, as well as integrating it into the interface for making the decision and make the knowledge
base more accessible to be used.

# Third Epoch (Outlook)

* starting 2020, December 28th
* finishing approximately 2021, late January

The goal of the third epoch is to finish the decision execution engine. What does this mean? Develop a
proof-of-concept for the manipulation of the thread environment data and use it for making automated 
decisions on transitions from one node to the next node.

Also develop the interfaces required to not only automatically process the transitions, but also everything 
what is required to process machine intelligent decision nodes, as well as human intelligent decision 
nodes.

 