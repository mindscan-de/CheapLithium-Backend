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

The Third Epoch became quite long as I thought I could split the parser stuff into the fouth Epoch,
but it became obvious to me that there would be no real progress until the parsing is done "correctly".

But after that, the integration in the whole system should be easy enough and clear enough.

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  ? Next ? Next ? Next ? Next ? Next ? Next ? Next ? Next ? Next ? Next ? Next ? Next ? Next ? Next ? Next ? Next ?
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

----------------------------------------------
The next Epoch: integrate the parser and the interpreter into the Execution Engine and remove all
preliminary parsing from the DecisionExecutionEngine.
----------------------------------------------

# Fourth Epoch (???)

Anyways a better user experience is also a way to go to next. Also better report generation and 
presentation capabilities is one of the next options we can take. It looks like the project will 
enter some kind of maintenance mode with eproch number 4. The heavy lifting seems to be done.

---------------------------
---------------------------