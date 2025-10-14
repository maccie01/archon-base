# Research Result: React Hooks Patterns

# React Hooks Patterns

**Main Takeaway:**

Comprehensive, TypeScript-based React Hooks implementations improve code maintainability, performance, and testability by encapsulating stateful logic, enforcing type safety, and enabling reusable, composable patterns.

## 1. Complex useState Scenarios

When state involves nested objects or arrays, prefer using functional updates and immutable patterns:

typescript<code>typeTodo={ id:string; text:string; done:boolean};

const[todos, setTodos]=useState<Todo[]>([]);

// Add item
const addTodo =useCallback((newTodo: Todo)=>{
setTodos(prev =>[...prev, newTodo]);
},[]);

// Toggle done
const toggleTodo =useCallback((id:string)=>{
setTodos(prev =>
    prev.map(todo =>
      todo.id === id ?{...todo, done:!todo.done }: todo
)
);
},[]);
</code>

## 2. useEffect Cleanup Patterns

Always return a cleanup function to avoid memory leaks or stale subscriptions:

typescript<code>useEffect(()=>{
const controller =newAbortController();
fetch(url,{ signal: controller.signal }).then(setData);
return()=> controller.abort();
},[url]);
</code>

Cleanup also applies to event listeners:

typescript<code>useEffect(()=>{
consthandleResize=()=>setWidth(window.innerWidth);
  window.addEventListener('resize', handleResize);
return()=> window.removeEventListener('resize', handleResize);
},[]);
</code>

## 3. Performance Optimization with useCallback & useMemo

* **useCallback** memoizes functions so they retain identity across renders.
* **useMemo** memoizes computed values to avoid expensive recalculations.

typescript<code>const expensiveValue =useMemo(()=>computeHeavy(data),[data]);

const handleClick =useCallback(()=>{
onAction(id);
},[onAction, id]);
</code>

## 4. useRef for DOM Access and Mutable Values

Use `useRef` to reference DOM nodes or persist mutable values without causing re-renders:

typescript<code>const inputRef =useRef<HTMLInputElement>(null);

constfocusInput=()=> inputRef.current?.focus();

useEffect(()=>{
  inputRef.current?.value = initialValue;
},[initialValue]);
</code>

## 5. useContext Usage

Context avoids prop drilling for global state:

typescript<code>interfaceAuthContextType{ user: User;login():void;logout():void;}
const AuthContext =createContext<AuthContextType |undefined>(undefined);

exportconstuseAuth=()=>{
const ctx =useContext(AuthContext);
if(!ctx)thrownewError('useAuth must be inside AuthProvider');
return ctx;
};
</code>

## 6. useReducer for Complex State

`useReducer` centralizes state transitions:

typescript<code>typeState={ count:number; step:number};
typeAction={ type:'increment'}|{ type:'setStep'; payload:number};

functionreducer(state: State, action: Action): State {
switch(action.type){
case'increment':return{...state, count: state.count + state.step };
case'setStep':return{...state, step: action.payload };
default:return state;
}
}

const[state, dispatch]=useReducer(reducer,{ count:0, step:1});
</code>

Combine with context for global reducers.

## 7. Custom Hooks Library

Example custom hooks:

## useDebounce

typescript<code>exportfunctionuseDebounce<T>(value:T, delay =300):T{
const[debounced, setDebounced]=useState(value);
useEffect(()=>{
const id =setTimeout(()=>setDebounced(value), delay);
return()=>clearTimeout(id);
},[value, delay]);
return debounced;
}
</code>

## useLocalStorage

typescript<code>exportfunctionuseLocalStorage<T>(key:string, initial:T){
const[state, setState]=useState<T>(()=>{
const stored = localStorage.getItem(key);
return stored ?JSON.parse(stored): initial;
});
useEffect(()=>{
    localStorage.setItem(key,JSON.stringify(state));
},[key, state]);
return[state, setState]asconst;
}
</code>

## useAsync

typescript<code>interfaceAsyncState<T>{ loading:boolean; data?:T; error?: Error;}
exportfunctionuseAsync<T>(fn:()=>Promise<T>, deps:any[]=[]){
const[state, setState]=useState<AsyncState<T>>({ loading:true});
useEffect(()=>{
let mounted =true;
fn()
.then(data => mounted &&setState({ loading:false, data }))
.catch(error => mounted &&setState({ loading:false, error }));
return()=>{ mounted =false;};
}, deps);
return state;
}
</code>

## 8. Hook Composition

Combine hooks to build higher-level abstractions:

typescript<code>functionuseFilteredDebouncedList<T>(
  list:T[],
filterFn:(item:T)=>boolean,
  query:string
){
const filtered =useMemo(()=> list.filter(filterFn),[list, filterFn]);
const debouncedQuery =useDebounce(query,300);
returnuseMemo(
()=> filtered.filter(item => item.includes(debouncedQuery)),
[filtered, debouncedQuery]
);
}
</code>

## 9. Hook Testing

Use `@testing-library/react-hooks`:

typescript<code>import{ renderHook, act }from'@testing-library/react-hooks';
import{ useCounter }from'./useCounter';

test('should increment counter',()=>{
const{ result }=renderHook(()=>useCounter(0));
act(()=>{ result.current.increment();});
expect(result.current.count).toBe(1);
});
</code>

Ensure `act()` wraps state updates to flush effects.