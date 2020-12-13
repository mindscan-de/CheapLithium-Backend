# CheapLithium-Backend

CheapLithium-Backend is a http based backend for the CheapLithium-Frontend. Most of my projects 
on github are completely private educational projects and aren't fit for any purpose whatsoever.

## The Idea

So what's the purpose then? The CheapLithium-Frontend is a browser based decision tree modelling 
tool. This project is the most simple backend, backed by files instead of a database, i could 
think of. It has no security in mind, nor an access concept nor any other fancy corporate grade 
nor consumer grade mechanics. I just need this tool.

This backend ist just enough to make the frontend work, but will be extended on a need-by-need basis.

This backend will also contain the execution engine of the decision trees and will collect 
information about the use and execution of the decision models. This is to prepare a dataset
will allow to predict the right decision model for the right problem, or the right analysis
(e.g. machine learning with multi classifiers in mind.)

Having a decision tree model or rather a DAG instead of a tree, helps a lot of course, but knowing
which decision model to use is even more important. Having thousands of decision models doesn't do
much, but you then have to implement decision models to decide which decision model to use, which
basically makes these small and many decision models a really big one.But instead of building the
big tree, we need to learn and dynamically adapt the big tree. 

Therefore data is needed. Maybe this will lead to an AI which will provide problem solving 
capabilities.

## The Current Path

I'm using FastAPI to implement the webserver callbacks really cheap. There are actually these
responsibilities on the backend side:

* store the decision model
* manipulate the decision model
* store the execution and its curent state of execution of the decision model (decision model runtime)
* manipulate the decision model runtime
* executing the decision model runtime (e.g. execute MIT - Machine intelligent tasks)
* store the knowledge base
* manipulate the knowledge base
* generate reports of executed models
** Statistics wise
** thread wise, to print out an analysis 

Therefore we have these 5 components right now - but also keep in mind, that I don't intend 
to develop all of them to the fullest, just enough to make the whole system work. I'm just 
one person. Therefore do not expect too much work being put into this whole idea.

* Modelling Engine
* Runtime Engine
* Knowledge Base Engine
* Exection engine
* Report Engine  