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

# Second Epoch (Outlook)

* starting 2020, December 21st
* finishing approx. 2021, second half of January

The second epochs goal is to create a ThreadReportGenerator, which will basically summarize what
decision were made during the decision process. I will collect requirements during that phase and
the "make it work" approach to identify the logging needs for the runtime engine to fulfil - to 
create a good report at the end of the execution of one decision tree.

So basically the idea is to make the ThreadReportGenerator work, with as little effort as possible,
and evolve the current code base to meet these new requirements. I threw all current requirements
out from the board, and decided for most of them to implement them later or never. Because i want
this report generator right now to work as convincing as possible.

Maybe I can implement most of the DecisionThreadEnvironment model and use its contents to create 
the reports. Most probably I will fake most of the DecisionThreadEnvironment at the start and then
implement the most urgent things in the DecisionExecutionEngine. Since I'm undecided how all these
automated signatures and evaluation functions will look like yet.

Also one major concern is the integration of the knowledge base into the modelling of the decision 
nodes, as well as integrating them into the interface for making the decision - but maybe, this will
be postponed untile the third epoch.