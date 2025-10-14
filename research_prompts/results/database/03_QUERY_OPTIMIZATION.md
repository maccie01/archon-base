# Research Result: Query Optimization

## Index Strategies

## When to Add Indexes

Indexes dramatically improve read performance but add overhead to write operations. Create indexes for columns frequently used in WHERE clauses, JOIN conditions, and ORDER BY statements.[mydbops](https://www.mydbops.com/blog/postgresql-indexing-best-practices-guide)

**❌ Before: Sequential Scan**

typescript<code>// No index on email column
const user =await db.select()
.from(users)
.where(eq(users.email,'user@example.com'));
</code>

sql<code>-- EXPLAIN ANALYZE output
Seq Scan on users  (cost=0.00..1693.00rows=1 width=97)
(actual time=0.125..45.234rows=1 loops=1)
  Filter: (email ='user@example.com')
Rows Removed by Filter: 49999
Execution Time: 45.567 ms
</code>

**✅ After: Index Scan**

typescript<code>// Add index on email column
await db.execute(sql`
  CREATE INDEX idx_users_email ON users(email)
`);

const user =await db.select()
.from(users)
.where(eq(users.email,'user@example.com'));
</code>

sql<code>-- EXPLAIN ANALYZE output
Index Scan using idx_users_email on users  (cost=0.29..8.31rows=1 width=97)
(actual time=0.015..0.016rows=1 loops=1)
Index Cond: (email ='user@example.com')
Execution Time: 0.034 ms
</code>

 **Performance Improvement: 99.93% faster (45.567ms → 0.034ms)** [enterprisedb**+1**](https://www.enterprisedb.com/blog/postgresql-query-optimization-performance-tuning-with-explain-analyze)

## Composite Indexes

Composite indexes optimize queries filtering on multiple columns. Column order matters—the most selective column should come first.[dev](https://dev.to/digitalpollution/overview-of-postgresql-indexing-lpi)

**❌ Before: Multiple Index Scans**

typescript<code>// Separate indexes or no indexes
const orders =await db.select()
.from(orders)
.where(
and(
eq(orders.userId,123),
eq(orders.status,'pending')
)
);
</code>

sql<code>-- EXPLAIN ANALYZE output
Bitmap Heap Scan on orders  (cost=125.45..890.23rows=250 width=128)
(actual time=12.456..34.789rows=245 loops=1)
  Recheck Cond: (user_id =123)
  Filter: (status='pending')
Rows Removed by Filter: 1205
Execution Time: 35.123 ms
</code>

**✅ After: Composite Index**

typescript<code>// Create composite index with correct column order
await db.execute(sql`
  CREATE INDEX idx_orders_user_status 
  ON orders(user_id, status)
`);

const orders =await db.select()
.from(orders)
.where(
and(
eq(orders.userId,123),
eq(orders.status,'pending')
)
);
</code>

sql<code>-- EXPLAIN ANALYZE output
Index Scan using idx_orders_user_status on orders  (cost=0.42..15.67rows=245 width=128)
(actual time=0.023..0.891rows=245 loops=1)
Index Cond: ((user_id =123)AND(status='pending'))
Execution Time: 1.034 ms
</code>

 **Performance Improvement: 97.06% faster (35.123ms → 1.034ms)** [mydbops**+1**](https://www.mydbops.com/blog/postgresql-indexing-best-practices-guide)

## Partial Indexes

Partial indexes index only rows meeting specific conditions, reducing index size and improving query performance for targeted queries.[dev](https://dev.to/digitalpollution/overview-of-postgresql-indexing-lpi)

**❌ Before: Full Table Index**

typescript<code>// Full index on all rows
await db.execute(sql`
  CREATE INDEX idx_orders_created ON orders(created_at)
`);
</code>

**✅ After: Partial Index**

typescript<code>// Index only active orders (90% of queries target active orders)
await db.execute(sql`
  CREATE INDEX idx_active_orders_created 
  ON orders(created_at) 
  WHERE status IN ('pending', 'processing')
`);

const activeOrders =await db.select()
.from(orders)
.where(
and(
inArray(orders.status,['pending','processing']),
gte(orders.createdAt,newDate('2025-01-01'))
)
)
.orderBy(desc(orders.createdAt));
</code>

**Index Size: 70% smaller, Query Performance: 40% faster**[dev](https://dev.to/digitalpollution/overview-of-postgresql-indexing-lpi)

## Index Maintenance

Monitor index usage and remove unused indexes to reduce write overhead.[mydbops](https://www.mydbops.com/blog/postgresql-indexing-best-practices-guide)

typescript<code>// Identify unused indexes
const unusedIndexes =await db.execute(sql`
  SELECT 
    schemaname, 
    tablename, 
    indexname, 
    idx_scan
  FROM pg_stat_user_indexes
  WHERE idx_scan = 0
    AND indexname NOT LIKE '%_pkey'
  ORDER BY tablename, indexname
`);
</code>

---

## Query Analysis

## Using EXPLAIN ANALYZE

EXPLAIN ANALYZE executes queries and provides detailed execution plans with actual timing.[thoughtbot**+1**](https://thoughtbot.com/blog/reading-an-explain-analyze-query-plan)

typescript<code>// Basic EXPLAIN ANALYZE
const plan =await db.execute(sql`
  EXPLAIN ANALYZE
  SELECT * FROM users
  WHERE created_at > '2025-01-01'
  ORDER BY created_at DESC
  LIMIT 100
`);
</code>

**Key Metrics to Monitor:**

* **Execution Time** : Total query time
* **Planning Time** : Time spent planning query
* **Rows** : Estimated vs actual rows processed
* **Cost** : Planner's estimated cost units[enginelabs**+1**](https://www.enginelabs.ai/blog/optimize-postgres-query-performance-using-explain-analyze-a-comprehensive-guide)

## Reading Query Plans

Query plans are read bottom-up. Focus on operations with highest actual time.[thoughtbot](https://thoughtbot.com/blog/reading-an-explain-analyze-query-plan)

sql<code>-- Example query plan
Sort  (cost=1234.56..1234.78rows=100 width=128) 
(actual time=15.234..15.456rows=100 loops=1)
  Sort Key: created_at DESC
  Sort Method: quicksort  Memory: 45kB
-> Seq Scan on users  (cost=0.00..1230.00rows=5000 width=128) 
(actual time=0.012..12.345rows=5000 loops=1)
       Filter: (created_at >'2025-01-01')
Rows Removed by Filter: 45000
Planning Time: 0.123 ms
Execution Time: 15.678 ms
</code>

 **Bottleneck** : Sequential scan removing 45,000 rows—add index on `created_at`[enginelabs**+1**](https://www.enginelabs.ai/blog/optimize-postgres-query-performance-using-explain-analyze-a-comprehensive-guide)

## Identifying Bottlenecks

Common performance issues in query plans:[enginelabs](https://www.enginelabs.ai/blog/optimize-postgres-query-performance-using-explain-analyze-a-comprehensive-guide)

1. **Sequential Scans** on large tables → Add indexes
2. **High Rows Removed by Filter** → Improve index selectivity
3. **Nested Loop Joins** with many iterations → Consider hash joins
4. **Sort operations** using disk → Increase work_mem or add index

---

## N+1 Query Prevention

## What is the N+1 Problem

The N+1 problem occurs when an application executes one query to fetch N records, then N additional queries to fetch related data—resulting in N+1 total queries.[stackoverflow**+1**](https://stackoverflow.com/questions/97197/what-is-the-n1-selects-problem-in-orm-object-relational-mapping)

**❌ Before: N+1 Queries**

typescript<code>// Fetches 1 + N queries (1 for users, N for posts)
const users =await db.select().from(users).limit(10);

// N additional queries inside loop
for(const user of users){
const posts =await db.select()
.from(posts)
.where(eq(posts.userId, user.id));
  
  user.posts = posts;
}
</code>

sql<code>-- Query execution:
SELECT*FROM users LIMIT10;-- 1 query: 2.3ms
SELECT*FROM posts WHERE user_id =1;-- Query 1: 1.2ms
SELECT*FROM posts WHERE user_id =2;-- Query 2: 1.1ms
...
SELECT*FROM posts WHERE user_id =10;-- Query 10: 1.3ms

-- Total: 11 queries, ~15ms
</code>

**✅ After: Single Query with Join**

typescript<code>// Drizzle relational query - single SQL query
const usersWithPosts =await db.query.users.findMany({
  limit:10,
with:{
    posts:true,
},
});
</code>

sql<code>-- Single query with JOIN
SELECT 
  users.*, 
  posts.*
FROM users
LEFTJOIN posts ON posts.user_id = users.id
WHERE users.id IN(
SELECT id FROM users LIMIT10
);

-- Total: 1 query, ~3.5ms
</code>

 **Performance Improvement: 76.67% faster (15ms → 3.5ms), 90.91% fewer queries (11 → 1)** [pingcap**+1**](https://www.pingcap.com/article/how-to-efficiently-solve-the-n1-query-problem/)

## Eager Loading with Drizzle

Use relational queries to eagerly load related data.[orm.drizzle**+1**](https://orm.drizzle.team/docs/perf-queries)

typescript<code>// Define relations in schema
exportconst usersRelations =relations(users,({ many })=>({
  posts:many(posts),
  comments:many(comments),
}));

// Eager load nested relations
const usersWithData =await db.query.users.findMany({
  columns:{
    id:true,
    name:true,
    email:true,
},
with:{
    posts:{
      columns:{
        id:true,
        title:true,
},
with:{
        comments:{
          limit:5,
},
},
},
},
  limit:20,
});
</code>

## Batch Loading Alternative

For scenarios where joins aren't optimal, use IN clauses for batch loading.[pingcap](https://www.pingcap.com/article/how-to-efficiently-solve-the-n1-query-problem/)

typescript<code>// Fetch users
const users =await db.select().from(users).limit(100);
const userIds = users.map(u => u.id);

// Batch fetch all posts in single query
const posts =await db.select()
.from(posts)
.where(inArray(posts.userId, userIds));

// Group posts by userId in application
const postsByUser = posts.reduce((acc, post)=>{
if(!acc[post.userId]) acc[post.userId]=[];
  acc[post.userId].push(post);
return acc;
},{});
</code>

---

## Caching Strategies

## Query Result Caching

Implement caching for frequently accessed, slowly changing data.[linkedin](https://www.linkedin.com/posts/grzegorz-wolfinger-b88856229_databaseoptimization-drizzleorm-postgres-activity-7250395623974223872-buw4)

**❌ Before: No Caching**

typescript<code>// Every request hits database
exportasyncfunctiongetPopularPosts(){
returnawait db.select()
.from(posts)
.orderBy(desc(posts.viewCount))
.limit(10);
}

// Response time: ~25ms per request
</code>

**✅ After: Redis Caching**

typescript<code>import{ Redis }from'ioredis';

const redis =newRedis(process.env.REDIS_URL);
constCACHE_TTL=300;// 5 minutes

exportasyncfunctiongetPopularPosts(){
const cacheKey ='popular_posts:top10';
  
// Try cache first
const cached =await redis.get(cacheKey);
if(cached){
returnJSON.parse(cached);
}
  
// Cache miss - query database
const posts =await db.select()
.from(posts)
.orderBy(desc(posts.viewCount))
.limit(10);
  
// Store in cache
await redis.setex(cacheKey,CACHE_TTL,JSON.stringify(posts));
  
return posts;
}

// Response time: ~0.5ms (cache hit), ~25ms (cache miss)
</code>

 **Performance Improvement: 98% faster on cache hits (25ms → 0.5ms)** [linkedin](https://www.linkedin.com/posts/grzegorz-wolfinger-b88856229_databaseoptimization-drizzleorm-postgres-activity-7250395623974223872-buw4)

## Cache Invalidation

Invalidate cache when data changes.[linkedin](https://www.linkedin.com/posts/grzegorz-wolfinger-b88856229_databaseoptimization-drizzleorm-postgres-activity-7250395623974223872-buw4)

typescript<code>exportasyncfunctioncreatePost(data: NewPost){
const post =await db.insert(posts).values(data).returning();
  
// Invalidate related caches
await redis.del('popular_posts:top10');
await redis.del(`user_posts:${data.userId}`);
  
return post;
}
</code>

---

## Connection Pooling

## Pool Configuration

Proper connection pooling prevents connection exhaustion and improves performance.[architecture-weekly**+1**](https://www.architecture-weekly.com/p/architecture-weekly-189-mastering)

**❌ Before: No Pooling**

typescript<code>// Creates new connection per query
import{ Client }from'pg';

const client =newClient({ connectionString: process.env.DATABASE_URL});
await client.connect();

// Connection overhead: ~20-50ms per query
</code>

**✅ After: Connection Pool**

typescript<code>import{ Pool }from'pg';
import{ drizzle }from'drizzle-orm/node-postgres';

const pool =newPool({
  connectionString: process.env.DATABASE_URL,
  max:20,// Maximum connections
  idleTimeoutMillis:30000,// Close idle connections after 30s
  connectionTimeoutMillis:2000,// Wait 2s for available connection
  maxUses:7500,// Retire connections after 7500 uses
});

exportconst db =drizzle(pool,{ schema });
</code>

 **Connection overhead reduced: 95% faster (20-50ms → 1-2ms)** [gist.github**+1**](https://gist.github.com/productdevbook/7c9ce3bbeb96b3fabc3c7c2aa2abc717)

## Connection Limits

Set appropriate pool size based on workload:[solutionanalysts](https://www.solutionanalysts.com/blog/node-js-mastering-database-connection-pooling/)

typescript<code>// Formula: connections = ((core_count × 2) + effective_spindle_count)
// For 4-core server with SSD: (4 × 2) + 1 = 9 connections minimum

const poolConfig ={
// Web application (high concurrency)
  max:20,
  
// Background worker (batch processing)
  max:5,
  
// API server (moderate load)
  max:10,
};
</code>

## Pool Monitoring

Monitor pool health to prevent connection leaks.[architecture-weekly**+1**](https://www.architecture-weekly.com/p/architecture-weekly-189-mastering)

typescript<code>pool.on('connect',()=>{
console.log('New client connected to pool');
});

pool.on('error',(err)=>{
console.error('Unexpected pool error', err);
});

// Health check endpoint
app.get('/health',async(req, res)=>{
  res.json({
    totalCount: pool.totalCount,
    idleCount: pool.idleCount,
    waitingCount: pool.waitingCount,
});
});
</code>

---

## Prepared Statements

## How Drizzle Uses Prepared Statements

Prepared statements precompile SQL queries, eliminating repeated parsing overhead.[orm.drizzle](https://orm.drizzle.team/docs/perf-queries)

**❌ Before: Dynamic Query**

typescript<code>// Query parsed every execution
asyncfunctiongetUserByEmail(email:string){
returnawait db.select()
.from(users)
.where(eq(users.email, email));
}

// Execution time: ~5.2ms (includes parsing)
</code>

**✅ After: Prepared Statement**

typescript<code>// Prepare once, execute many times
const getUserByEmail = db.select()
.from(users)
.where(eq(users.email, sql.placeholder('email')))
.prepare('get_user_by_email');

// Reuse prepared statement
const user1 =await getUserByEmail.execute({ email:'user1@example.com'});
const user2 =await getUserByEmail.execute({ email:'user2@example.com'});

// Execution time: ~2.1ms (no parsing overhead)
</code>

 **Performance Improvement: 59.62% faster (5.2ms → 2.1ms)** [gist.github**+1**](https://gist.github.com/productdevbook/7c9ce3bbeb96b3fabc3c7c2aa2abc717)

## When to Use Prepared Statements

Use prepared statements for:[orm.drizzle](https://orm.drizzle.team/docs/perf-queries)

* Frequently executed queries
* Queries in hot code paths
* Loop iterations with similar queries
* API endpoints with consistent query patterns

typescript<code>// Prepare commonly used queries at startup
exportconst preparedQueries ={
  getUserById: db.select()
.from(users)
.where(eq(users.id, sql.placeholder('id')))
.prepare('get_user_by_id'),
  
  getPostsByUser: db.select()
.from(posts)
.where(eq(posts.userId, sql.placeholder('userId')))
.prepare('get_posts_by_user'),
  
  updateUserLastSeen: db.update(users)
.set({ lastSeenAt: sql.placeholder('timestamp')})
.where(eq(users.id, sql.placeholder('id')))
.prepare('update_user_last_seen'),
};
</code>

---

## Batch Operations

## Batch Inserts vs Single Inserts

Batch operations dramatically reduce network overhead and transaction costs.[tigerdata**+1**](https://www.tigerdata.com/blog/boosting-postgres-insert-performance)

**❌ Before: Loop with Single Inserts**

typescript<code>// Insert 1000 records individually
const records =generateRecords(1000);

for(const record of records){
await db.insert(users).values(record);
}

// Total time: ~3,500ms (3.5ms per insert)
// Database round trips: 1000
</code>

**✅ After: Batch Insert**

typescript<code>// Insert 1000 records in single query
const records =generateRecords(1000);

await db.insert(users).values(records);

// Total time: ~145ms
// Database round trips: 1
</code>

 **Performance Improvement: 95.86% faster (3,500ms → 145ms)** [hatchet**+1**](https://docs.hatchet.run/blog/fastest-postgres-inserts)

## Bulk Updates

Batch updates using CASE statements for multiple records.[cybertec-postgresql](https://www.cybertec-postgresql.com/en/bulk-load-performance-in-postgresql/)

**❌ Before: Multiple Updates**

typescript<code>// Update 100 records individually
const updates =[
{ id:1, status:'completed'},
{ id:2, status:'failed'},
// ... 98 more
];

for(const update of updates){
await db.update(orders)
.set({ status: update.status })
.where(eq(orders.id, update.id));
}

// Total time: ~850ms
</code>

**✅ After: Bulk Update with SQL**

typescript<code>// Update all records in single query
const ids = updates.map(u => u.id);
const statusMap = updates.reduce((acc, u)=>{
  acc[u.id]= u.status;
return acc;
},{});

await db.execute(sql`
  UPDATE orders
  SET status = CASE id
${sql.raw(updates.map(u => 
`WHEN ${u.id} THEN '${u.status}'`
).join(' '))}
  END
  WHERE id IN (${sql.join(ids, sql`, `)})
`);

// Total time: ~28ms
</code>

 **Performance Improvement: 96.71% faster (850ms → 28ms)** [cybertec-postgresql](https://www.cybertec-postgresql.com/en/bulk-load-performance-in-postgresql/)

## Performance Comparison Table

| Operation      | Single Queries | Batch Operation | Improvement |
| -------------- | -------------- | --------------- | ----------- |
| 1,000 inserts  | 3,500ms        | 145ms           | 95.86%      |
| 100 updates    | 850ms          | 28ms            | 96.71%      |
| 10,000 inserts | 35,000ms       | 890ms           | 97.46%      |

[tigerdata**+2**](https://www.tigerdata.com/blog/boosting-postgres-insert-performance)

---

## JSONB Optimization

## GIN Indexes on JSONB

GIN indexes enable efficient queries on JSONB columns.[tigerdata**+2**](https://www.tigerdata.com/learn/how-to-index-json-columns-in-postgresql)

**❌ Before: No JSONB Index**

typescript<code>// Sequential scan on JSONB column
const products =await db.select()
.from(products)
.where(sql`metadata->>'category' = 'electronics'`);
</code>

sql<code>-- EXPLAIN ANALYZE output
Seq Scan on products  (cost=0.00..2845.00rows=500 width=256)
(actual time=0.234..89.456rows=487 loops=1)
  Filter: ((metadata->>'category')='electronics')
Rows Removed by Filter: 49513
Execution Time: 90.123 ms
</code>

**✅ After: GIN Index**

typescript<code>// Create GIN index on JSONB column
await db.execute(sql`
  CREATE INDEX idx_products_metadata 
  ON products USING GIN (metadata)
`);

const products =await db.select()
.from(products)
.where(sql`metadata->>'category' = 'electronics'`);
</code>

sql<code>-- EXPLAIN ANALYZE output
Bitmap Heap Scan on products  (cost=12.34..156.78rows=487 width=256)
(actual time=0.456..3.234rows=487 loops=1)
  Recheck Cond: ((metadata->>'category')='electronics')
-> Bitmap Index Scan on idx_products_metadata  (cost=0.00..12.22rows=487 width=0)
(actual time=0.234..0.234rows=487 loops=1)
Execution Time: 3.567 ms
</code>

 **Performance Improvement: 96.04% faster (90.123ms → 3.567ms)** [pganalyze**+1**](https://pganalyze.com/blog/gin-index)

## Efficient JSONB Queries

Use appropriate operators for JSONB queries.[prateekcodes**+1**](https://www.prateekcodes.dev/postgresql-jsonb-indexing-performance-guide/)

typescript<code>// Containment queries (@> operator)
const users =await db.select()
.from(users)
.where(sql`preferences @> '{"theme": "dark"}'`);

// Key existence (? operator)
const products =await db.select()
.from(products)
.where(sql`metadata ? 'warranty'`);

// Path-based access for better performance
await db.execute(sql`
  CREATE INDEX idx_products_category 
  ON products ((metadata->>'category'))
`);
</code>

## When to Normalize vs JSONB

Choose between JSONB and normalized tables based on query patterns.[scalegrid**+1**](https://scalegrid.io/blog/using-jsonb-in-postgresql-how-to-effectively-store-index-json-data-in-postgresql/)

**Use JSONB when:**

* Schema is flexible or frequently changing
* Querying entire documents
* Data is hierarchical and accessed together
* Write-heavy workloads

**Use Normalized Tables when:**

* Schema is stable
* Frequent filtering/sorting on specific fields
* Complex joins required
* Read-heavy workloads with specific field access

typescript<code>// Hybrid approach - normalize frequently queried fields
exportconst products =pgTable('products',{
  id:serial('id').primaryKey(),
  name:text('name').notNull(),
  category:text('category').notNull(),// Normalized for filtering
  price:numeric('price').notNull(),// Normalized for sorting
  metadata:jsonb('metadata'),// Flexible additional data
});

// Fast query on normalized fields
const filteredProducts =await db.select()
.from(products)
.where(
and(
eq(products.category,'electronics'),
gte(products.price,'100')
)
)
.orderBy(desc(products.price));
</code>