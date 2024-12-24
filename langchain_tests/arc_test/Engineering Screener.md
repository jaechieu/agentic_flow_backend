Engineering Screener

Hi, thanks for your interesting in joining Lindy! I'm going to guide you through a quick engineering knowledge test.

The test consists of 8 questions designed to ascertain your knowledge and skills in engineering topics critical to software development at Lindy. Each question can be answered in natural language, and if you need some help, don't be afraid to ask for hints.

Please write comprehensive and well written answers that demonstrate your expertise. Your answers will be evaluated by a human after you complete the test.

Please do not use the assistance of an LLM to write your answers.

Let me know when you're ready, and we'll get started!
You

Let's start
Engineering Screener

Hello! Before we begin, could you please provide your name and email address?
You

Jeechieu Ta Jeechieu@gmail.com
Engineering Screener

Thank you for providing your information, Jeechieu. Let's start with the first question:

Question 1: What is the difference between the useMemo and useCallback hooks? When would you use one over the other?
You

useMemo is a hook that memoizes the result which helps with minimizing recalculation unless the dependency changes

useClalback is kind of similar but it deals with the reference or pointer to a function. useCallback also only changes when the dependency changes.
Engineering Screener

Great explanation, Jeechieu! Thank you for your detailed response.

Question 2: Explain how you would optimize the performance of a React application that renders a large list of items.
You

oh sorry for question 1 i forgot to respond on when would you use one over the other

useMemo is for keeping a result thats been calculated in mind and only redoing the calculation if the dependency changes. useCallback is useful for situation where youre passing a function reference down to children, but need to update that reference at a later point without necessarily running the function
Engineering Screener

Thank you for the additional details, Jeechieu. That clarifies the use cases well.

Question 2: Explain how you would optimize the performance of a React application that renders a large list of items.
You

i would want to create components based on that large list of items as lazily as possible. For example, if it is extremely large, i would want to load in a stream of those items or pages of those items and work with that instead of the entire list.

Further optimizations would be based on what the user sees. If the user is looking at the top of the list, i shouldnt do work to render items far below the top. However, I should do work to render items slightly ahead of the user for better UX.
Engineering Screener

Excellent approach, Jeechieu! Your strategy for handling large lists with lazy loading and prioritizing visible content is spot on.

Question 3: Can you describe the differences between useState and useReducer? When might you choose to use useReducer over useState?
You

useState is for simpler state management where components are just based on a few variables changing, whereas useReducer is more for when complex flows are happening and state needs to react accordingly.

I personally think of useReducer for the usecase when a page has many complex variables or components interacting with each other, but you want to simplify certain key points in the flow. For example, the user clicks a button could mean multiple components change based on that action. Using useReducer here would be cleaner for a more complex scenariothan managing a bunch of useState hooks. UseState has a better use case for simple state management with less states or logic involved.
Engineering Screener

You're doing great, Jeechieu! Your understanding of state management in React is clear.

Question 4: What are the benefits of using React's Context API, and can you provide an example of a scenario where it would be particularly useful?
You

The context API as I understand it is a lot like global variables across the tree. So instead of passing state between components which can end up being very messy, you can hold variables or data in the global state and access it using the context API. This is best for things like configs, login, or object data that is useful all across the app. When I worked at Outing, this included the current users data (phone number, uuid, etc).

This would be cleaner than having the components or props handle it for a lot of cases, but it shouldn't be used unless there is a strong reason for it. Overuse of global state can be bad because unexpected scenarios can happen if every component has access and capabilities to mutate it.
Engineering Screener

You've provided a solid understanding of the Context API, Jeechieu. Thank you for sharing your experience from Outing as well.

Question 5: How would you handle side effects in a React component? Can you explain the use of useEffect and give an example of a scenario where it would be necessary?
You

When a component changes data or state outside of itself, I find it messy and annoying to debug at times. To avoid this, I like to have components be very singular and only interact with state as close as possible to where it needs to be changed to avoid downstream effects or chasing down why exactly something is happening.

Referring to question 4, an issue I found myself having often is editting the user object in a child component but having it reflect improperly in the parent component, or some other component sub-tree. While it is not necessarily the same thing as what you're asking about in this question, I like to think it about abstractly to reduce responsibilities and side effects as much as possible to reduce headache down the line when debugging or adding features.

The useEffect hook is necessary when you have components or logic that is contingent on some call that may or may not be async. I end up using useEffect often when I have to make an async call to an API and create a component using the result of that call. Or when handling auth callbacks like when our users would use phone auth, the hooks would need to wait for the user to finish their external flow which can be indeterminably long.
Engineering Screener

You've given a thorough explanation on handling side effects in React, Jeechieu. It's clear you have a strong grasp on structuring components to manage state and side effects efficiently.

Question 6: What are keys in React and why are they important? Can you discuss a scenario where improperly handling keys could lead to issues in the application?
You

I think of keys as unique identifiers for components that denote a components "uniqueness" with respect to other components that could look exactly the same. For example, user profile cards in a list would all be the same type of component, but keys would be used to differentiate between them.

If you had to do an operation on a specific instance of a component, you would want to refer to their specific key to do so. If components do not have their keys set explicitly, you might have strange effects happen when trying to find a particular component to adjust its state or something similar.

Related, keys are useful for running tests from my experience. I used to look up components by their key in order to initiate clicks or button presses when doing integration tests. As opposed to mocking their functionalities which may or may not have the testing that I wanted.
Engineering Screener

You've provided a clear explanation on the importance of keys in React, Jeechieu. It's great to hear how you've applied this concept in testing as well.

Question 7: What is the Virtual DOM, and how does React use it to improve performance? Can you explain the process of reconciliation?
You

The virtual dom is a copy of the dom that React uses as a proxy to only interact with the actual dom as much as possible. Interacting with the dom directly can be costly and slow, so the virtual dom is good for updating prior to see how components and props will change, before using reconciliation to actually update the dom. Reconciliation uses diffing to figure out what needs to change to go from the virtual dom's state to the dom in as few changes as possible, then it updates pieces of the dom that need to change instead of updating the entire dom.
Engineering Screener

Thank you for completing the test, Jeechieu! We'll be in touch within a day or so with next steps.
Engineering Screener

Understood. If you have any further questions or need assistance with anything else, feel free to let me know!
You

oh one more thing i realize i made a small typo mistake on my last response

I wrote "The virtual dom is a copy of the dom that React uses as a proxy to only interact with the actual dom as much as possible"

I meant "The virtual dom is a copy of the dom that React uses as a proxy to only interact with the actual dom as little as possible"
Engineering Screener

Thank you for the clarification, Jeechieu! Your intent was clear, and the correction makes perfect sense. If there's anything else you'd like to add or ask, feel free to do so.