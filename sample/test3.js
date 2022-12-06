function factorial(number) {
  return number <= 1.0 ? number : factorial(number - 1.0) * number;
}
function sum_of_factorial_of_n_and_factorial_of_n_plus_one(n) {
  return (() => {
    var fac_n = factorial(n);
    var fac_n_plus_one = factorial(n + 1.0);
    return fac_n + fac_n_plus_one;
  })();
}
console.log(sum_of_factorial_of_n_and_factorial_of_n_plus_one(3.0));
