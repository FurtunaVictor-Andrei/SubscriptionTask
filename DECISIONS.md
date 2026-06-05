**What I built and what I skipped.**
1. Writen something for every endpoint described. For testing I asked Gemini to help
me create a GUI for testing what I have done.

**Ambiguities**
1. The most confusing one was the webhook/billing endpoint. I went with the option
of not creating a new id for the subscription as I don't think it's useful given the fact
that there already is an unique id for every user.
2. I also find unclear whether the cancel button should refund the money paid or just 
strip the Premium title, I chose just to take away the Premium title

**Storage Choice**

For storage I chose RAM memory because I did not want to fill sql tables with testing
information. Data was transmitted through JSON file format between frontend and backend
and stored on RAM in the same format.

**The given scenario answer**

When the cancel endpoint is called it turns the state to "Standard"
no matter what the previous state was, meaning that it turns from "Standard" to "Standard" and then
to "Premium" when the call for the subscribe endpoint finally arrives, so the subscription isn't
canceled. To this I have a solution in mind: Make the function from the API recall itself
after 30s - 1min. Ex: Cancel arrived at 14:00:01, Subscribe arrived at 14:00:02, Cancel recalled
at 14:00:31 and now the subscription is canceled. I also believe this  will do great in testing
because the cancel will most certainly come last even if we subscribe and cancel many times.

**Edge cases**
1. I don't check whether the user is already subscribed or not - don't think that it affects the code
to much in this state, in the future will be good to add a checker for the subscription plan.
2. I also don't check the clock synchronization for the grace period because of the RAM storage option,
I can't change the date manually to see what happens when the clock reaches 0, but partially tried 
to handle it in code.

**If I had more time...**

I would change the storage to database, add the refund money option, add an option
to create an user (auth not required but register will be useful).

**AI usage**
1. I created the "skeleton" of this code, wrote what I knew (created the endpoints and classes 
and some of their logic) and then asked Gemini how and what to change to connect it properly with
the frontend.
2. Encountered many problems with the creation of the graphic interface but helped me the most in this task
3. Gemini first attempt called the API but didn't use it's endpoints, just displayed hardcoded information.
