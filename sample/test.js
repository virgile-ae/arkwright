function factorial(n) {
  return ((n != 1.0) ? (n * factorial((n - 1.0))) : n)
}
console.log(factorial(4.0))
let counter = 0.0;
counter = (counter + 1.0)
console.log(counter)
function do_n_times(fn, n) {
  return (() => { let array_of_n = Array(n);
  array_of_n = array_of_n.fill()
  return array_of_n.map(fn)
})()
}
do_n_times(function _() {
  return console.log("hello world")
}, 4.0)