// server.js
const jsonServer = require('json-server');
const server = jsonServer.create();
const router = jsonServer.router('db.json');
const middlewares = jsonServer.defaults();

// Map `page` -> `_page` and `per_page` -> `_limit`
server.use((req, res, next) => {
  if (req.query && req.query.page && !req.query._page) {
    req.query._page = req.query.page;
    delete req.query.page;
  }
  if (req.query && req.query.per_page && !req.query._limit) {
    req.query._limit = req.query.per_page;
    delete req.query.per_page;
  }
  next();
});

server.use(middlewares);
server.use(router);

const PORT = process.env.PORT || 3001;
server.listen(PORT, () => {
  console.log(`json-server with param mapping on http://localhost:${PORT}`);
  console.log(`Try: http://localhost:${PORT}/users?page=1&per_page=50`);
});
