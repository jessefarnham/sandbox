import matplotlib.pyplot as plt
import sys

class TaxBracket(object):

    def __init__(self, min_income, max_income, rate):
        assert 0 <= min_income < max_income
        assert rate >= 0
        self._min_income = min_income
        self._max_income = max_income
        self._rate = rate

    def get_tax(self, taxable_income):
        income_over_min = max(taxable_income - self._min_income, 0)
        bracket_size = self._max_income - self._min_income
        income_within_bracket = min(income_over_min, bracket_size)
        return income_within_bracket * self._rate

    @property
    def rate(self):
        return self._rate

    @property
    def min_income(self):
        return self._min_income

    @property
    def max_income(self):
        return self._max_income


def _check_brackets(b1, b2):
    if b1:
        assert b1.max_income == b2.min_income
        assert b1.rate < b2.rate


class TaxPlan(object):

    def __init__(self, brackets, deduction):
        self._brackets = brackets
        self._deduction = deduction
        assert self._deduction >= 0
        reduce(_check_brackets, self._brackets)

    def get_tax(self, total_income):
        taxable_income = max(total_income - self._deduction - self._get_exemption(), 0)
        tax = sum([bracket.get_tax(taxable_income) for bracket in self._brackets])
        return tax

    def _get_exemption(self):
        return 4050


TRUMP = TaxPlan(
    [
        TaxBracket(0, 37500, .12),
        TaxBracket(37500, 112500, .25),
        TaxBracket(112500, sys.float_info.max, .33)
    ], 15000
)


CURRENT = TaxPlan(
    [
        TaxBracket(0, 9275, .1),
        TaxBracket(9275, 37650, .15),
        TaxBracket(37650, 91150, .25),
        TaxBracket(91150, 190150, .28),
        TaxBracket(190150, 413350, .33),
        TaxBracket(413350, 415050, .35),
        TaxBracket(415050, sys.float_info.max, .4),
    ], 6300
)


def main():
    plt.figure()
    plt.subplot(211)
    plt.title('Single, standard deduction, no dependents')
    plt.ylabel('Tax')
    plt.xlabel('Income')
    tax_results = {}
    for name, plan in ('trump', TRUMP), ('current', CURRENT):
        incomes, taxes = [], []
        for i in range(0, int(500000), 1000):
            incomes.append(i)
            taxes.append(plan.get_tax(i))
        color = 'b' if name == 'current' else 'r'
        plt.plot(incomes, taxes, color, label=name)
        tax_results[name] = taxes
    plt.legend()
    plt.subplot(212)
    plt.plot(incomes, [c - t for t, c in zip(tax_results['trump'], tax_results['current'])])
    plt.title('Trump plan advantage')
    plt.show()


def test_trump():
    assert TRUMP.get_tax(0) == 0
    assert TRUMP.get_tax(19050) == 0
    assert TRUMP.get_tax(119050) == 20125



if __name__ == '__main__':
    main()
