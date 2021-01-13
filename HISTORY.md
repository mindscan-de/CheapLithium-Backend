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

As of 2021, january 2nd speaking,

The third epochs goal was to implement major parts of the decision execution engine. We are now able
to store a default environment for a model, have thread environment data, and are able to access these
values. We are also able to execute the transition methods (lets call them guards), evaluate their 
outcome and provide extra data for the report, collected from the environment. The transitions can 
be evaluated by considering runtime values found in the runtime environment data of the thread. An
invocation of the guard-method can have zero or more input parameters.

Also the default thread start environment is calculated and used when a thread is started. 

* starting 2021, January 03rd 
* finishing approximately 2021, late January

Also develop the interfaces required to not only automatically process the transitions, but also everything 
what is required to process machine intelligent decision nodes, as well as human intelligent decision 
nodes.

* starting 2021, January 09th

I started with implementing the tokenizer and parser from January 9th. Main reason for it, is that i
wanted to avoid to fill my code with more provisoric code, which would be to just to make the runtime 
engine work. Therefore I reordered the priorities to finish some of the requirements, so that the 
Tokenizer/Parser/Interpreter will be used instead of propietary and temporary solutions. Such work
arounds will also make a later transition more difficult. The minimal viable product will just enable 
to execute the guard and ignore the data manipulation body.



# Fourth Epoch (???)

There are quite a few things how this project can be developed further. Rewriting the runtime execution
parsing to use ASTs would be a huge step forward, since it allows better developement of models in the
browser as well as in the backend. Anyways a better user experience is also a way to go to next. Also 
better report generation and presentation capabilities is one of the next options we can take. It looks
like the project will enter some kind of maintenance mode with eproch number 4. The heavy lifting seems
to be done.