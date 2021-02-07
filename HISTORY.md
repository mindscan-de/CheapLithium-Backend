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

# Third Epoch (Done)

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
* finishing approximately 2021, end of January

Also develop the interfaces required to not only automatically process the transitions, but also everything 
what is required to process machine intelligent decision nodes, as well as human intelligent decision 
nodes.

* starting 2021, January 09th

I started with implementing the tokenizer and parser from January 9th. Main reason for it, is that i
wanted to avoid to stuff my code with even more provisoric code, which would be to just to make the 
runtime engine work. Therefore I reordered the priorities to finish some of the requirements, so that 
the Tokenizer/Parser/Interpreter will be used instead of proprietary and temporary solutions. Such work-
arounds will also make a later transition more difficult. The minimal viable product will just enable 
to execute the guard and ignore the data manipulation body.

* starting 2021, January 13th

I started the parser and the ast nodes and the interpreter mid of January. The main objective was to 
first develop the AST node structure and a working interpreter for it despite lacking the parser. It
turned out to be okay and working good enough to rely on that AST structure and to test some ideas 
which node types are useful and which node properties might be useful. 

* starting 2021, January, 17th

Procrastinated long enough to not implement the parser... Well... Since all other things are somehow
done kind of okay... I had to start the parser now... But i wasn't satisfied how it started and my
building a compiler courses were back some time. But luckily I still found things to do in the 
interpreter... 

* starting 2021, January, 20th

I found a solution to parse the UI out of the method body and also started to implement a way to
either generate the user interface or to evaluate its "results". So I introduced the SpecialEngine
which will evolve into some global RuntimeEnvironment/ExecutionEnvironment soon. Now that i can 
inject and modify the runtime behavior while execution i don't need to bother to compile the ast 
with different generators for different usecases. (e.g render the userinterface, use the user 
input and inject it into the runtime environment)

* starting 2021, January 24th

I decided to develop the grammar and test the grammar with xtext and write grammar unit tests outside
of this project, by basically creating an XText project and starting from a simple production grammar.
From this point in time it was then just offloading all obvious implementations and implement all the 
things which were easy enough at this point in time. The more time I spent on it it became obvious how
the parser infrastructure should work and then it was test driven development. By the way, the tests 
were very useful a lot of times, since I failed a lot, but i was glad to catch these failures as early
as i wrote the code.     

* starting 2021, January 30th

I finalized implementing the parsing of the grammar and now it is time to do the full integration 
step, which connects the tokenizer, the ast, the parser and the interpreter into one working entity.
Since I changed my mind quite often what kind of nodes to implement, a bit of minor adaptions had to 
be made - all over the code and the unit tests as well. Anyways I was quite satisfied with this result.
Later in time I know I will have to add more grammar rules and maybe rewrite the parser, but now since
I had done it again after a few years I feel quite comfortable to maybe do it once more or twice.

The development gained traction after the parsing was done and I started writing integration level
tests to make the components work together better and find more errors and finish things up. I also
solved the assignment problem which was bugging me how to perform the calculation of the reference 
in case of an value on the left side of the equal sign.

The Third Epoch became quite long as I thought I could split the parser stuff into the fouth Epoch,
but it became obvious to me that there would be no real progress until the parsing is done "correctly".

But after that, the integration in the whole system should be easy enough and clear enough.

* starting 2021, January 31st
* finishing 2021, February 2nd.

I was able to finish the integration of the UI and the Backend, such that a thread can be executed 
and user data can be provided and such. This is quite a major step forward. It turns out, that the 
system needs some kind of IDE-Mode since doing everything in each one dialog has disadvantages, that 
will interrupt a nice workflow. But I will leave that for another epoch. 

Anyways I'm quite satisfied with the outcome. Now it is time again to work more on the frontend and
its backend support rather to work only on the backend sider of the project.

The Third Epoch became quite long as I thought previously I could delay the parser stuff into the 
fouth Epoch, but it became obvious to me that there would be no real progress until the parsing is 
done "correctly". And viewing back, this was the right choice. I could also remove a lot of 
preliminary code, which was there to make the UI work as early as possible.  

Fourth Epoch

* starting 2021, February 1st
* finished 2021, February 7th

I can't say whether the fourth epoch started on February first or, but it was quite a seamless 
transition, where the main objective is to integrate the parser, the interpreter into the Decision-
ExecutionEngine and remove all the obsolete and preliminary code.

The main goal is to improve the user experience as fast as possible. And to provide a full demo 
case of the intended use of the whole system. It looks like the main part of the heavy lifting is 
done by now, but it doesn't mean there is nothing to improve. I will mainly work on the estimator
model, and i will also hopefully gain some experience using my own system (apply some dogfooding).

So the next steps are report generation, since this was also one of the goals of the whole system.

Later down the line I think I will work on the knowledge base system. Maybe i can also work on
some quantitative analysis of the runtime of a thread to provide estimates how much time is consumed
for each step.


* starting 2021, February 3rd 

Use the same color scheme for the xgml export as in the web application. 

Added some functionality to create and combine the reports. The data of the mini reports for the transition 
is now inserted into the templates and he GUI was extended to help to generate a report for a thread. 

Also the error handling was improved by a lot, because the runtime exceptions are now accessible through the
web interface itself. Which hopefully helps to find modelling issues earlier.


>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  ? Next ? Next ? Next ? Next ? Next ? Next ? Next ? Next ? Next ? Next ? Next ? Next ? Next ? Next ? Next ? Next ?
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

So what's next?

I regard this modelling tool currently as good enough and I think I will shift my attention to 
other projects I'm working on. I will try to use this tool and see whether it will provide me
some of the projected benefits to me. 

If this tool is developed to a more user-type and project-manager-type audience instead of the
current hands-on (this code) developer-type audience it needs developed further to be more of a
help to the people defining and developing new models and developing vm-parts of the code which 
will help to automatize and do the analysis. Also serving this to other means that a whole 
information channel of the console will nt be seen, so everything must become even more robust.

For compley and asynchronous tasks there should also be a complete overhaul of the engine and 
the storage of the threads and such.

For Project management
* How much was it?
** calculate the time from start to end
** calculate the time for each node and caclulcate more statistics
** Which paths are/were never taken?

For Optimization and AI
* Always prefer smaller models over larger models
* calculate which models are executed after others to have some bayesian predictions for future processing 

For Ticket-Analysis
* allow to continue with different models, if one of the models already provided basic analysis. 
  You should be able to continue with a more precise model each time.
* the system should allow "uploads" and then do analysis on the given data, which will open a 
  whole new dimension to make it into a "Analysis as a Service" - AAAS - System

For Developers
* Provide a language server so that it can 
** check Syntax / maybe even interactively (red or green while typing)
** make suggestions / autocomplete
** AST
* Provide A user defined start-Environment to keep interactions with the user low during the execution of the model
* Some kind of IDE Mode, where you can make more changes in parallel instead of having an interactive dialog
  for each of them
* maybe provide a DSL, which can generate models from a demain specific language. Such that the developer of
  models doesn't have to do the laborous work using each and every dialog.
  
For Knowledge Workers
* provide a better "Wiki" and syntax and a rendering engine for the Knowledge Base, which then also 
  can be used to create/improve/render the reports.
  
Some Decision Thread model related stuff like
* Finish and resume threads
* Archive finished threads
* continue with other decision threads

Some Usability stuff
* some interactive Selections and filters (e.g. Search for a decision thread) 

----

For the moment I'm undecided on how to develop that system further and what will provide the most 
benefit as for the users speaking. Everything above is a way to go, but some of these points are
more useful than others in the short term. As for now, i will give that project some time to mature
in my head. But nevertheless, I think that this project, were well spent 11 weeks of my spare time.

I had some time to hone my skills, on topics I learned years ago, so this was a good refresher 
for some of the topics, such as implementing the whole tokenizer, ast, parser, interpreter and 
runtime for a graph based modelling tool, for just providing the ability for executing and script 
the decision tree elements.