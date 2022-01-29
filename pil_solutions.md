[home](./index.md)
-------------------

*author: niplav, created: 2022-01-08, modified: 2022-01-08, language: english, status: in progress, importance: 2, confidence: likely*

> __Solutions to the book “Programming in Lua” by Roberto
Ierusalimschy.__

Solutions to “Programming in Lua”
==================================

Chapter 1
----------

### Exercise 1.1

	function fact(n)
		elseif n==0 then
			return 1
		else
			return n * fact(n-1)
		end
	end

	print("enter a number:")
	a=io.read("*n")
	print(fact(a))

### Exercise 1.2

For a script that loads a library the dofile option is probably
preferable, since then there is no need to deal with the different ways
different platforms handle flags, when using lua interactively, the '-l'
option is nicer, since one needs to type less.

### Exercise 1.3

Actually, from the top of my head, I really can't. But apparently<!--TODO:
link-->, Haskell does it, which is weird, since Lua and Haskell have
pretty different lineages afaik.

### Exercise 1.4

Valid identifiers from the list: `___`, `_end`, `End`, `NULL`

Invalid identifiers: `end`, `until?`, `nil`

### Exercise 1.5

	#!/usr/bin/lua
	print(arg[0])

Then, update the permissions (on a unix-based system):

	$ chmod 0755 ex_5.lua

Chapter 2
----------

### Exercise 2.1

The result of the expression `type(nil)==nil` is `false`, since the type
of `type(nil)` is `string`, and the string `"nil"` is not equal to the
value `nil`.

### Exercise 2.2

Invalid numerals: `.e12`, `0.0e`, `0xABFG`, `FFFF`, `0x`

Valid numerals (with value): `.0e12` -> `0.0`, `0x12` -> `18`, `0xA` ->
`10`, `0xFFFFFFFF` -> `4294967295`, `0x1P10` -> `1024`, `0.1e1` -> `1.0`,
`0x0.1p1` -> `0.125`

### Exercise 2.3

12.7 can't be represented by

	(n*12.7)/2^m

but 5.5 can be represented by

	11/2^1

### Exercise 2.4

	a="<![CDATA[\n  Hello world\n]]>"
	b=[=[
	<![CDATA[
	  Hello world
	]]>]=]

### Exercise 2.5

One good way to format the sequence of bytes would be to display it in a
string with escaped bytes in hexadecimal format, split into several lines
with `"\z"`. By doing this problems with line length can be avoided and
performance is probably not very bad, considering that computers handle
byte sequences considerably well. Readability can, but should not be a
problem, since when dealing with arbitrary byte sequences the value in
hexadecimal is used more frequently than the ASCII value.

### Exercise 2.6

	a={}
	a.a=a

`a.a.a.a` evaluates to the table a the first `a` is a pointer to the
table `a`, the other `a`s are all keys the expression can be rewritten as
`a["a"]["a"]["a"]``

	a.a.a.a=3

Now the value for the key `"a"` is 3 in the table `a`, so `a.a` is 3,
and `a.a.a` is not indexable, since 3 has no field called `"a"`. So Lua
prints an error message.

Chapter 3
----------

### Exercise 3.1

	-10 2
	-9 0
	-8 1
	-7 2
	-6 0
	-5 1
	-4 2
	-3 0
	-2 2
	-1 1
	0 0
	1 1
	2 2
	3 0
	4 1
	5 2
	6 0
	7 1
	8 2
	9 0
	10 1

### Exercise 3.2

	2^3^4=2^(3^4)=1.4178e+24
	2^-3^4=(2^(-(3^4))=4.1359e-25

### Exercise 3.3

	function polyeval(a, x)
		local res=0
		for i=1, #a do
			res=res+a[i]*x^(i-1)
		end
		return res
	end

### Exercise 3.4

	function polyeval(a, x)
		local res=0
		for i=1, #a do
			res=res*x
			res=res+a[i]
		end
		return res
	end

### Exercise 3.5

	function isbool(v)
		return v==true or v==false
	end

### Exercise 3.6

The parentheses are not necessary, since `not` binds stronger than
`and`, and `and` binds stronger than `or`. However, the parentheses are
probably still a good idea, since they make the expression easier to
read and understand.

### Exercise 3.7

	monday	sunday	sunday

### Exercise 3.8

One way to initialize the table would be to use the square bracket
notation. Associating the escape sequence `"\a"` with the literal bell
character would be done like this:

	{["\\a"]="\a"}

This would be done for every escape sequence.

Chapter 4
----------

### Exercise 4.1

In Lua there is no switch/case statement, so elseif is a necessary
(albeit not sufficient) replacement.

### Exercise 4.2

Preferred method is the first one, since it doesn't deal with limits
and makes an infinite loop clear from the beginning.

	while true do end

	for i=0, math.huge do end

	for i=2, 1, 0 do end

	repeat until false

### Exercise 4.3

repeat-until is a construct similar to do-while in C, a construct which
is also used rarely there. Apparently, in C only 5% of loops in C code are
do-while loops. However, repeat-until can be useful to avoid initializing
a variable the same way it is incremented in the loop, saving one line.
It makes elegant solutions easier, but not much beyond that, so it could
be left out easily.

### Exercise 4.4

	local z = 0
	local c

	repeat
		c = io.read()
		if c == '0' then z=z+1 end
		print(z)
	until c == nil

	if z % 2 == 0 then
		print('ok')
	else
		print('not ok')
	end

### Exercise 4.5

Jumping out of a function would jump into the scope of a local variable,
which is not possible (per definition) in Lua.

This would also cause problems in a function calling itself and
jumping back into itself (or two different functions calling each other
recursively), since there would be no good way to determine whether the
goto would simply jump inside the function or outside into a previous
call of itself.

### Exercise 4.6

The program would first print:

	10
	9
	8
	7
	6
	5
	4
	3
	2
	1

and then return an anonymous function that jumps to the end of getlabel()
and return 0.

Chapter 5
----------

### Exercise 5.1

	function concat(...)
		local args={...}
		local r=""
		for i, v in ipairs(args) do
			r=r..v
		end
		return r
	end

### Exercise 5.2

	function printarr(arr)
		print(table.unpack(arr))
	end

### Exercise 5.3

	function allbutone(...)
		local r={}
		local args=table.pack(...)
		for i=2, args.n do
			r[i-1]=args[i]
		end
		return table.unpack(r)
	end

### Exercise 5.4

	function combi(t, n)
		local arg={}
		local res={}
		local save={}

		if n<=0 then
			return {{}}
		end

		for k, v in ipairs(t) do save[k]=v end

		while #save>0 do
			local last=save[#save]
			save[#save]=nil

			for k, v in ipairs(save) do table.insert(arg, v) end

			local tmp=combi(arg, n-1)
			arg={}

			for i=1, #tmp do table.insert(tmp[i], last) end
			for k, v in ipairs(tmp) do table.insert(res, v) end
		end
		return res
	end

	function comb(t)
		local res={}
		for i=1, #t do
			tmp=combi(t, i)
			for k, v in ipairs(tmp) do table.insert(res, tmp[k]) end
		end
		return res
	end

Chapter 6
----------

### Exercise 6.1

	function integral(f)
		return function(x, y)
			local i, res, eps
			res=0; eps=0.001
			for i=x, y, eps do
				res=res+f(i)*eps
			end
			return res
		end
	end

### Exercise 6.2

	function newpoly(t)
		return function(x)
			local res=0
			for i=1, #t do
				res=res+t[i]*x^(#t-i)
			end
			return res
		end
	end

### Exercise 6.3

	n=100000

	function f()
		print(n)
		n=n-1
		if n<0 then
			return nil
		else
			return "i=1;"
		end
	end

	load(f)()

### Exercise 6.4

	function room1()
		local move=io.read()
		if move=="south" then room3()
		elseif move=="east" then room2()
		else
			print("invalid move")
			room1()
		end
	end

	function room2()
		local move=io.read()
		if move=="south" then room4()
		elseif move=="west" then room1()
		else
			print("invalid move")
			room2()
		end
	end

	function room3()
		local move=io.read()
		if move=="north" then room1()
		elseif move=="east" then room4()
		else
			print("invalid move")
			room3()
		end
	end

	function room4()
		print("Congrats, asshat. You won.")
	end

	room1()

Chapter 7
----------

### Exercise 7.1

	function fromto(n, m)
		return fromit, {m}, n-1
	end

	function fromit(t, v)
		if v<t[1] then
			return v+1
		else
			return nil
		end
	end

### Exercise 7.2

	function fromto(n, m, s)
		return fromit, {m, s}, n-s
	end

	function fromit(t, v)
		if v+t[2]<=t[1] then
			return v+t[2]
		else
			return nil
		end
	end

### Exercise 7.3

	function uniquewords()
		local line=io.read()
		local wordtable={}
		local pos=1
		wordtable[""]=1
		return function()
			local str=""
			local s, e
			repeat
				s, e=string.find(line, "%w+", pos)
				if s then
					pos=e+1
					str=str.sub(line, s, e)
				else
					line=io.read()
					pos=1
				end
			until not line or wordtable[str]~=1
			wordtable[str]=1
			return (line and str) or nil
		end
	end

### Exercise 7.4

	function substrings(s)
		local len, pos
		len=0
		pos=1
		return function()
			if pos+len>#s then
				pos=pos+1
				len=0
			end
			if pos>#s then
				return nil
			else
				local str=string.sub(s, pos, pos+len)
				len=len+1
				return str
			end
		end
	end

Chapter 8
----------

### Exercise 8.1

`s` is definitely a string, `c` can be a string or a function

	function loadwithprefix(s, c)
		return load(function ()
			local t
			if s then
				t=s
				s=nil
			elseif type(c)=="string" then
				t=c
				c=nil
			elseif type(c)=="function" then
				t=c()
			end
			return t
		end)
	end

### Exercise 8.2

	function multiload(...)
		local t=table.pack(...)
		local i=1
		return load(function ()
			local res
			if i>#t then
				return nil
			end
			if type(t[i])=="string" then
				i=i+1
				return t[i-1]
			end
			while not res and i<=#t do
				res=t[i]()
				i=i+1
			end
			return res
		end)
	end

### Exercise 8.3

The two functions have nearly the same speed.

	function stringrep_n(n)
		local res=[[	s=...
		local r=""
	]]
		if n>0 then
			while n>1 do
				if n%2~=0 then res=res .. "\tr=r .. s\n" end
				res=res .. "\ts=s .. s\n"
				n=math.floor(n/2)
			end
			res=res .. "\tr=r .. s\n"
		end
		res=res .. "\treturn r\n"
		return load(res)
	end

### Exercise 8.4

Shamelessly stolen (years later, I don't know where from, though :-D):

	function f()
		count = 0
		function g()
			count = count + 1
			if count == 2 then debug.sethook() end
			error()
		end
		debug.sethook(g, "r")
	end

with

	pcall(pcall, f)

returns `false`, `nil`.

Chapter 9
----------

### Exercise 9.1

	function combgen(t, n, r, i)
		local idx=i or 1
		local res=r or {}

		if n<=0 then
			coroutine.yield(res)
		else
			for j=idx, #t-n do
				res[n]=t[j]
				combgen(t, n-1, res, j+1)
			end
		end
	end

	function combinations(t, n)
		return coroutine.wrap(function() combgen(t, n) end)
	end

### Exercise 9.2

	socket=require("socket")

	function download(host, file)
		local c=assert(socket.connect(host, 80))
		local count=0
		c:send("GET " .. file .. " HTTP/1.0\r\n\r\n")
		while true do
			local s, status=receive(c)
			count=count+#s
			if status=="closed" then break end
		end
		c:close()
		print(file, count)
	end

	function receive(connection)
		connection:settimeout(0)
		local s, status, partial=connection:receive(2^10)
		if status=="timeout" then
			coroutine.yield(connection)
		end
		return s or partial, status
	end

	function get(host, file)
		local co=coroutine.create(function()
		download(host, file)
		end)
		table.insert(threads, co)
	end

	function dispatch()
		local i=1
		local timedout={}
		while true do
			if threads[i]==nil then
				if threads[1]==nil then break end
				i=1
				timedout={}
			end
			local status, res=coroutine.resume(threads[i])
			if not res then
				table.remove(threads, i)
			else
				i=i+1
				timedout[#timedout+1]=res
				if #timedout==#thredas then
					socket.select(timedout)
				end
			end
		end
	end

	threads={}

### Exercise 9.3

	function transfer(cr)
		coroutine.yield(cr)
	end

	function dispatch(b)
		nr=coroutine.create(b)
		while nr~=nil do
			nr=coroutine.resume(nr)
		end
	end

Chapter 10
-----------

### Exercise 10.1

	local N=8

	local function isplaceok(a, n, c)
		for i=1, n-1 do
			if (a[i]==c) or
			   (a[i]-i==c-n) or
			   (a[i]+i==c+n) then
				return false
			end
		end
		return true
	end

	local function printsolution(a)
		for i=1, N do
			for j=1, N do
				io.write(a[i]==j and "X" or "-", " ")
			end
			io.write("\n")
		end
		io.write("\n")
		os.exit()
	end

	local function addqueen(a, n)
		if n>N then
			printsolution(a)
		else
			for c=1, N do
				if isplaceok(a, n, c) then
					a[n]=c
					addqueen(a, n+1)
				end
			end
		end
	end

	addqueen({}, 1)

### Exercise 10.2

	local N=8

	function permgen(a, n)
	        n=n or #a
	        if n<=1 then
	                coroutine.yield(a)
	        else
	                for i=1, n do
	                        a[n], a[i]=a[i], a[n]
	                        permgen(a, n-1)
	                        a[n], a[i]=a[i], a[n]
	                end
	        end
	end

	function permutations(a)
	        return coroutine.wrap(function() permgen(a) end)
	end

	local function isplaceok(a, n, c)
	        for i=1, n-1 do
	                if (a[i]==c) or
	                   (a[i]-i==c-n) or
	                   (a[i]+i==c+n) then
	                        return false
	                end
	        end
	        return true
	end

	local function printsolution(a)
	        for i=1, N do
	                for j=1, N do
	                        io.write(a[i]==j and "X" or "-", " ")
	                end
	                io.write("\n")
	        end
	        io.write("\n")
	end

	for q in permutations({1, 2, 3, 4, 5, 6, 7, 8}) do
		local i=1
		while i<N+1 and isplaceok(q, i, q[i]) do i=i+1 end
		if i==N+1 then printsolution(q) end
	end

### Exercise 10.3

	local function allwords()
		local auxwords=function()
			for line in io.lines() do
				for word in string.gmatch(line, "%w+") do
					coroutine.yield(word)
				end
			end
		end
		return coroutine.wrap(auxwords)
	end

	local counter={}
	for w in allwords() do
		if #w>=4 then
			counter[w]=(counter[w] or 0) + 1
		end
	end

	local words={}
	for w in pairs(counter) do
		words[#words+1]=w
	end

	table.sort(words, function(w1, w2)
		return counter[w1]>counter[w2] or
			counter[w1]==counter[w2] and w1<w2
	end)

	for i=1, (tonumber(arg[1]) or 10) do
		print(words[i], counter[words[i]])
	end

### Exercise 10.4

	local N=3

	function allwords()
		local line=io.read()
		local pos=1
		return function()
			while line do
				local s, e=string.find(line, "%w+", pos)
				if s then
					pos=e+1
					return string.sub(line, s, e)
				else
					line=io.read()
					pos=1
				end
			end
			return nil
		end
	end

	function prefix(p)
		local s=p[1]
		for i=2, #p do s=s .. " " .. p[i] end
		return s
	end

	function back(p)
		for i=1, N-1 do p[i]=p[i+1] end
	end

	local statetab={}

	function insert(index, value)
		local list=statetab[index]
		if list==nil then
			statetab[index]={value}
		else
			list[#list+1]=value
		end
	end

	local MAXGEN=10000
	local NOWORD="\n"

	pf={}
	for i=1, N do pf[i]=NOWORD end

	for w in allwords() do
		insert(prefix(pf), w)
		back(pf)
		pf[N]=w
	end

	insert(prefix(pf), NOWORD)

	for i=1, N do pf[i]=NOWORD end

	for i=1, MAXGEN do
		local ls=statetab[prefix(pf)]
		local r=math.random(#ls)
		local nextword=ls[r]
		if nextword==NOWORD then return end
		io.write(nextword, " ")
		back(pf)
		pf[N]=nextword
	end

Chapter 11
-----------

### Exercise 11.1

It's stupid to set both values to 0. This just restores the first state.

queue={}

	function queue.new()
		return {first=0, last=-1}
	end

	function queue.pushfirst(q, value)
		q[q.first]=value
		q.first=q.first+1
	end

	function queue.pushlast(q, value)
		q[q.last]=value
		q.last=q.last-1
	end

	function queue.popfirst(q)
		local first=q.first-1
		if q.last>first then error("queue is empty") end
		local value=q[first]
		q[first]=nil
		q.first=first
		if q.last>=q.first-1 then q.first=0; q.last=-1 end
		return value
	end

	function queue.poplast(q)
		local last=q.last+1
		if last>q.first then error("queue is empty") end
		local value=q[last]
		q[last]=nil
		q.last=last
		if q.last>=q.first-1 then q.first=0; q.last=-1 end
		return value
	end

### Exercise 11.2

Using a closure for the allwords argument

	local function allwords(f)
		local auxwords=function()
			for line in io.lines(f) do
				for word in string.gmatch(line, "%w+") do
					coroutine.yield(word)
				end
			end
		end
		return coroutine.wrap(auxwords)
	end

	local ignore={}
	for w in allwords(arg[2] or "ignore") do
		ignore[w]=true
	end

	local counter={}
	for w in allwords() do
		if not ignore[w] then
			counter[w]=(counter[w] or 0) + 1
		end
	end

	local words={}
	for w in pairs(counter) do
		words[#words+1]=w
	end

	table.sort(words, function(w1, w2)
		return counter[w1]>counter[w2] or
			counter[w1]==counter[w2] and w1<w2
	end)

	for i=1, (tonumber(arg[1]) or 10) do
		print(words[i], counter[words[i]])
	end

### Exercise 11.3

	function name2node(graph, name)
		local node=graph[name]
		if not node then
			node={name=name, adj={}}
			graph[name]=node
		end
		return node
	end

	function readgraph(f)
		local graph={}
		for line in io.lines(f) do
			local namefrom, nameto, label=string.match(line, "(%S+)%s+(%S+)%s+(%d+)")
			local from=name2node(graph, namefrom)
			local to=name2node(graph, nameto)
			from.adj[to]=label
		end
		return graph
	end

	function findpath(curr, to, path, visited)
		path=path or {}
		visited=visited or {}
		if visited[curr] then
			return nil
		end
		visited[curr]=true
		path[#path+1]=curr
		if curr==to then
			return path
		end
		for node in pairs(curr.adj) do
			local p=findpath(node, to, path, visited)
			if p then return p end
		end
		path[#path]=nil
	end

	function printpath(path)
		for i=1, #path do
			print(path[i].name)
		end
	end

### Exercise 11.4

* `g`: the graph
* `s`: the name of the starting point
* `e`: the name of the endpoint

	dofile("ex_3.lua")

	function dijkstra(g, s, e)
		local unvisited={}
		local dist={}
		local prev={}
		local start=g[s]
		local lst=g[e]
		local current=start

		for i, j in pairs(g) do unvisited[j]=true end
		for i, j in pairs(g) do dist[j]=math.huge end

		dist[start]=0
		while current~=lst do
			for to, l in pairs(current.adj) do
				if unvisited[to]==true then
					local ndist=dist[current]+l
					if dist[to]>ndist then
						dist[to]=ndist
						prev[to]=current
					end
				end
			end

			unvisited[current]=false
			current=lst
			for i, j in pairs(unvisited) do
				if j==true and dist[i]<dist[current] then
					current=i
				end
			end
		end

		return prev
	end

Chapter 12
-----------

### Exercise 12.1

	function serialize(o, l)
		l=l or 1
		if type(o)=="number" then
			io.write(string.format("%a", o))
		elseif type(o)=="string" then
			io.write(string.format("%q", o))
		elseif type(o)=="table" then
			io.write("{\n")
			for k, v in pairs(o) do
				io.write(string.rep("\t", l))
				serialize(k, l+1)
				io.write("=")
				serialize(v, l+1)
				io.write(",\n")
			end
			io.write(string.rep("\t", l-1) .. "}")
			if l==1 then io.write("\n") end
		else
			error("cannot serialize a " .. type(o))
		end
	end

### Exercise 12.2

	function serialize(o, l)
		l=l or 1
		if type(o)=="number" then
			io.write(string.format("%a", o))
		elseif type(o)=="string" then
			io.write(string.format("%q", o))
		elseif type(o)=="table" then
			io.write("{\n")
			for k, v in pairs(o) do
				io.write(string.rep("\t", l) .. "[")
				serialize(k, l+1)
				io.write("] = ")
				serialize(v, l+1)
				io.write(",\n")
			end
			io.write(string.rep("\t", l-1) .. "}")
			if l==1 then io.write("\n") end
		else
			error("cannot serialize a " .. type(o))
		end
	end

### Exercise 12.3

	function serialize(o, l)
		l=l or 1
		if type(o)=="number" then
			io.write(string.format("%a", o))
		elseif type(o)=="string" then
			io.write(string.format("%q", o))
		elseif type(o)=="table" then
			io.write("{\n")
			for k, v in pairs(o) do
				io.write(string.rep("\t", l))
				if type(k)~="string" or not isidentifier(k) then io.write("[") end
				if type(k)=="string" and isidentifier(k) then io.write(k)
				else serialize(k, l+1) end
				if type(k)~="string" or not isidentifier(k) then io.write("]") end
				io.write(" = ")
				serialize(v, l+1)
				io.write(",\n")
			end
			io.write(string.rep("\t", l-1) .. "}")
			if l==1 then io.write("\n") end
		else
			error("cannot serialize a " .. type(o))
		end
	end

	function isidentifier(s)
		return string.match(s, "^[a-zA-Z_][a-zA-Z0-9_]*$")
	end

### Exercise 12.4

	function serialize(o, l)
		l=l or 1
		if type(o)=="number" then
			io.write(string.format("%a", o))
		elseif type(o)=="string" then
			io.write(string.format("%q", o))
		elseif type(o)=="table" then
			local i=1
			io.write("{\n")
			if o[i]~=nil then
				io.write(string.rep("\t", l))
				while o[i]~=nil do serialize(o[i]); io.write(", "); i=i+1 end
				io.write("\n")
			end
			for k, v in pairs(o) do
				if type(k)~="number" or k<1 or k>i then
					io.write(string.rep("\t", l))
					if type(k)~="string" or not isidentifier(k) then io.write("[") end
					if type(k)=="string" and isidentifier(k) then io.write(k)
					else serialize(k, l+1) end
					if type(k)~="string" or not isidentifier(k) then io.write("]") end
					io.write(" = ")
					serialize(v, l+1)
					io.write(",\n")
				end
			end
			io.write(string.rep("\t", l-1) .. "}")
			if l==1 then io.write("\n") end
		else
			error("cannot serialize a " .. type(o))
		end
	end

	function isidentifier(s)
		return string.match(s, "^[a-zA-Z_][a-zA-Z0-9_]*$")
	end
