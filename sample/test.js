function factorial(n) {
  return ((n != 1.0) ? (n * factorial((n - 1.0))) : n)
}
console.log(factorial(4.0))
let counter = 0.0;
counter = (counter + 1.0)
console.log(counter)