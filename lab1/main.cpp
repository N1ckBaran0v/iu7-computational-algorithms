#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>

#define EPS 0.0001

struct table_line_t {
    double x, y, dy;
};

std::vector<table_line_t> read_table(const char *filename);
void print_table(std::vector<table_line_t> &table);
void print_compar_table(std::vector<table_line_t> &table, double x);
void print_root_table(std::vector<table_line_t> &table, size_t n);
void find_system_solution();
double ans_newton(std::vector<table_line_t> &table, size_t n, const double x);
double ans_hermit(std::vector<table_line_t> &table, size_t n, const double x);

int main(void) {
    double x;
    size_t n;
    std::vector<table_line_t> table = read_table("table.txt");
    print_table(table);
    std::cout << "Введите x: ";
    std::cin >> x;
    std::cout << "Введите n: ";
    std::cin >> n;
    if (n + 1 > table.size()) 
        std::cout << "Ошибка! Невозможно построить полином такой степени из-за недостаточного количества точек!\n"; 
    else {
        if (x < table[0].x || x > table.back().x) 
            std::cout << "Внимание! Произошла экстраполяция!\n";
        std::cout << "Ответ при интерполяции Ньютона: " << ans_newton(table, n, x) << "\n";
        std::cout << "Ответ при интерполяции Эрмита: " << ans_hermit(table, n, x) << "\n";
        print_compar_table(table, x);
        print_root_table(table, n);
        find_system_solution();
    }
    return 0;
}

std::vector<table_line_t> read_table(const char *filename) {
    std::ifstream input(filename);
    std::vector<table_line_t> table;
    table_line_t tmp;
    while (input >> tmp.x >> tmp.y >> tmp.dy) 
        table.push_back(tmp);
    input.close();
    std::sort(table.begin(), table.end(), 
              [](const table_line_t &first, const table_line_t &second){
                  return first.x < second.x;
              });
    return table;
}

void print_table(std::vector<table_line_t> &table) {
    std::cout << "------------------------------------------\n";
    std::cout << "|   №   |     X    |     Y    |    Y'    |\n";
    std::cout << "------------------------------------------\n";
    std::cout.setf(std::ios::fixed);
    std::cout.precision(3);
    for (size_t i = 0; i < table.size(); ++i) {
        std::cout << '|';
        std::cout.width(7);
        std::cout << i + 1 << '|';
        std::cout.width(10);
        std::cout << table[i].x << '|';
        std::cout.width(10);
        std::cout << table[i].y << '|';
        std::cout.width(10);
        std::cout << table[i].dy << "|\n";
        std::cout << "------------------------------------------\n";
    }
}

void print_compar_table(std::vector<table_line_t> &table, double x) {
    std::cout << "-------------------------------\n";
    std::cout << "|Степень|   Ньютона|    Эрмита|\n";
    std::cout << "-------------------------------\n";
    std::cout.setf(std::ios::fixed);
    std::cout.precision(3);
    for (size_t i = 0; i < 5; ++i) {
        std::cout << '|';
        std::cout.width(7);
        std::cout << i + 1 << '|';
        std::cout.width(10);
        std::cout << ans_newton(table, i + 1, x) << '|';
        std::cout.width(10);
        std::cout << ans_hermit(table, i + 1, x) << "|\n";
        std::cout << "-------------------------------\n";
    }
}

void print_root_table(std::vector<table_line_t> &table, size_t n) {
    std::vector<table_line_t> copy_table = table;
    for (size_t i = 0; i < copy_table.size(); ++i) {
        std::swap(copy_table[i].x, copy_table[i].y);
        copy_table[i].dy = 1 / copy_table[i].dy;
    }
    std::sort(copy_table.begin(), copy_table.end(), 
              [](const table_line_t &first, const table_line_t &second){
                  return first.y < second.y;
              });
    std::cout << "Корень при интерполяции Ньютона: " << ans_newton(copy_table, n, 0) << "\n";
    std::cout << "Корень при интерполяции Эрмита: " << ans_hermit(copy_table, n, 0) << "\n";
}

void find_system_solution() {
    size_t n = 3;
    std::ifstream input("tableyx.txt");
    std::vector<table_line_t> tableyx;
    table_line_t tmp{0, 0, 0};
    while (input >> tmp.y >> tmp.x) 
        tableyx.push_back(tmp);
    input.close();
    std::sort(tableyx.begin(), tableyx.end(), 
              [](const table_line_t &first, const table_line_t &second){
                  return first.x < second.x;
              });
    input.open("tablexy.txt");
    std::vector<table_line_t> tablexy;
    while (input >> tmp.x >> tmp.y) 
        tablexy.push_back(tmp);
    input.close();
    std::sort(tablexy.begin(), tablexy.end(), 
              [](const table_line_t &first, const table_line_t &second){
                  return first.x < second.x;
              });
    std::vector<table_line_t> table(tablexy.size());
    for (size_t i = 0; i < tablexy.size(); ++i) {
        table[i].y = tablexy[i].x;
        table[i].x = tablexy[i].y - ans_newton(tableyx, n, table[i].y);
    }
    double ansx = ans_newton(table, n, 0);
    double ansy = ans_newton(tablexy, n, ansx);
    std::cout << "Приближенное решение системы: [" << ansx << ", " << ansy << "]\n"; 
}

double ans_newton(std::vector<table_line_t> &table, size_t n, const double x) {
    if (n + 1 > table.size())
        throw "Interpolation error";
    std::vector<double> x_table(n + 1, 0);
    std::vector<std::vector<double> > y_table(n + 1);
    table_line_t tmp{x, 0, 0};
    auto it0 = std::lower_bound(table.begin(), table.end(), tmp, 
                               [](const table_line_t &first, const table_line_t &second){
                                   return first.x < second.x;
                               });
    auto it1 = it0;
    it1++;
    bool need_back = false;
    for (size_t i = 0; i <= n; ++i, need_back = (need_back) ? false : true) {
        if (need_back && it0 != table.begin())
            --it0;
        else
            ++it1;
    }
    for (size_t i = 0; i <= n; ++i, ++it0) {
        y_table[i].resize(n + 1);
        x_table[i] = it0->x;
        y_table[i][0] = it0->y;
    }
    for (size_t i = 0; i < n; ++i) {
        for (size_t j = 0; j < n - i; ++j)
            y_table[j][i + 1] = (y_table[j][i] - y_table[j + 1][i]) / (x_table[j] - x_table[j + 1 + i]);
    }
    double xp = 1;
    double ans = 0;
    //std::cout << "Start\n";
    for (size_t i = 0; i < n + 1; ++i) {
        //std::cout << ans << ' ' << xp << '\n';
        ans += y_table[0][i] * xp;
        //std::cout << "X: " << x << ' ' << x_table[i] << '\n';
        xp *= x - x_table[i];
    }
    //std::cout << ans << ' ' << xp << '\n';
    return ans;
}

double ans_hermit(std::vector<table_line_t> &table, size_t n, const double x) {
    if (n + 1 > table.size())
        throw "Interpolation error";
    std::vector<double> x_table(2 * n + 2, 0);
    std::vector<std::vector<double> > y_table(2 * n + 2);
    table_line_t tmp{x, 0, 0};
    auto it0 = std::lower_bound(table.begin(), table.end(), tmp, 
                               [](const table_line_t &first, const table_line_t &second){
                                   return first.x < second.x;
                               });
    auto it1 = it0;
    it1++;
    bool need_back = false;
    for (size_t i = 0; i <= n; ++i, need_back = (need_back) ? false : true) {
        if (need_back && it0 != table.begin())
            --it0;
        else
            ++it1;
    }
    for (size_t i = 0; i <= n; ++i, ++it0) {
        y_table[2 * i].resize(2 * (n + 1));
        y_table[2 * i + 1].resize(2 * (n + 1));
        x_table[2 * i] = it0->x;
        x_table[2 * i + 1] = it0->x;
        y_table[2 * i][0] = it0->y;
        y_table[2 * i + 1][0] = it0->y;
        y_table[2 * i][1] = it0->dy;
    }
    for (size_t i = 0; i < n; ++i, ++it0)
        y_table[2 * i + 1][1] = (y_table[2 * i + 1][0] - y_table[2 * i + 2][0]) / (x_table[2 * i + 1] - x_table[2 * i + 2]);
    for (size_t i = 2; i < 2 * n + 2; ++i) {
        for (size_t j = 0; j < 2 * n + 2 - i; ++j)
            y_table[j][i] = (y_table[j][i - 1] - y_table[j + 1][i - 1]) / (x_table[j] - x_table[j + i]);
    }
    double xp = 1;
    double ans = 0;
    for (size_t i = 0; i < n + 1; ++i) {
        ans += y_table[0][i] * xp;
        xp *= x - x_table[i];
    }
    return ans;
}