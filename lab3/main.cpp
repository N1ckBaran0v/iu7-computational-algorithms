#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <cmath>

#define EPS 0.0001

struct table_line_t {
    double x, y;
};

struct table_3d_line_t {
    int x, y, z, u;
};

std::vector<table_3d_line_t> read_table(const char *filename);
void print_table(std::vector<table_3d_line_t> &table);
void solve(std::vector<table_3d_line_t> &table, double x, double y, double z, size_t s1, size_t s2, size_t s3);
double ans_newton(std::vector<table_line_t> &table, const double x, size_t n = 3);
double ans_spline(std::vector<table_line_t> &table, const double x, const double c0 = 0, const double cn = 0);

std::ostream &operator<<(std::ostream &out, std::vector <double> vec) {
    for (size_t i = 0; i < vec.size(); ++i)
        out << vec[i] << ' ';
    out << '\n';
    return out;
}

std::istream &operator>>(std::istream &in, std::vector <int> &vec) {
    for (size_t i = 0; i < vec.size(); ++i)
        in >> vec[i];
    return in;
}

int main(void) {
    double x, y, z;
    std::vector<table_3d_line_t> table = read_table("table.txt");
    print_table(table);
    std::cout << "Введите x: ";
    std::cin >> x;
    std::cout << "Введите y: ";
    std::cin >> y;
    std::cout << "Введите z: ";
    std::cin >> z;
    if (x < table[0].x || x > table.back().x ||
        y < table[0].y || y > table.back().y ||
        z < table[0].z || z > table.back().z) {
        std::cout << "Произошла экстраполяция.\n";
        return -1;
    }
    size_t s[3];
    size_t size = size_t(round(pow(table.size(), 0.333)));
    for (size_t i = 0; i < 3; ++i) {
        if (i == 0)
            std::cout << "0-" << size - 1 << " - Полином Ньютона введенной степени.\n" << size << " - Кубический сплайн.\nИначе - до свидания!\n";
        std::cout << "Выберите, какой метод применять на " << i + 1 << " этапе: ";
        std::cin >> s[i];
        if (s[i] > size) {
            std::cout << "Ладно, пока.\n";
            return -2;
        }
    }
    solve(table, x, y, z, s[0], s[1], s[2]);
    /*std::cout << "Ответ при интерполяции Ньютона: " << ans_newton(table, x) << "\n";
    std::cout << "Ответ при интерполяции кубическим сплайном (1): " << ans_spline(table, x) << "\n";
    std::cout << "Ответ при интерполяции кубическим сплайном (2): " << ans_spline(table, x, ans_newton(table, table[0].x, true)) << "\n";
    std::cout << "Ответ при интерполяции кубическим сплайном (3): " << ans_spline(table, x, ans_newton(table, table[0].x, true), ans_newton(table, table.back().x, true)) << "\n";*/
    return 0;
}

std::vector<table_3d_line_t> read_table(const char *filename) {
    std::ifstream input(filename);
    std::vector<table_3d_line_t> table;
    table_3d_line_t tmp;
    size_t nx, ny, nz;
    input >> nx >> ny >> nz;
    for (size_t k = 0; k < nz; k++) {
        std::vector <int> x(nx);
        input >> tmp.z >> x;
        for (size_t j = 0; j < ny; ++j) {
            input >> tmp.y;
            for (size_t i = 0; i < nx; ++i) {
                tmp.x = x[i];
                input >> tmp.u;
                table.push_back(tmp);
            }
        }
    }
    input.close();
    std::sort(table.begin(), table.end(), 
              [](const table_3d_line_t &first, const table_3d_line_t &second) {
        if (first.z != second.z)
            return first.z < second.z;
        if (first.y != second.y)
            return first.y < second.y;
        if (first.x != second.x) 
            return first.x < second.x;
        return first.u < second.u;
    });
    return table;
}

void print_table(std::vector<table_3d_line_t> &table) {
    std::cout << "---------------------\n";
    std::cout << "| № | X | Y | Z | U |\n";
    std::cout << "---------------------\n";
    for (size_t i = 0; i < table.size(); ++i) {
        std::cout << '|';
        std::cout.width(3);
        std::cout << i + 1 << '|';
        std::cout.width(3);
        std::cout << table[i].x << '|';
        std::cout.width(3);
        std::cout << table[i].y << '|';
        std::cout.width(3);
        std::cout << table[i].z << '|';
        std::cout.width(3);
        std::cout << table[i].u << '|';
        std::cout << "\n---------------------\n";
    }
}

void solve(std::vector<table_3d_line_t> &table, double x, double y, double z, size_t s1, size_t s2, size_t s3) {
    std::vector <table_line_t> tx, ty, tz;
    double ans;
    size_t size = size_t(round(pow(table.size(), 0.333)));
    tx.resize(size);
    ty.resize(size);
    tz.resize(size);
    //table_line_t tmp;
    for (size_t k = 0, it = 0; k < size; ++k) {
        tz[k].x = table[it].z;
        for (size_t j = 0; j < size; ++j) {
            ty[j].x = table[it].y;
            for (size_t i = 0; i < size; ++i, ++it) {
                tx[i].x = double(table[it].x);
                tx[i].y = double(table[it].u);
            }
            if (s1 < size) {
                ty[j].y = ans_newton(tx, x, s1);
            } else {
                ty[j].y = ans_spline(tx, x);
            }
        }
        if (s2 < size) {
            tz[k].y = ans_newton(ty, y, s2);
        } else {
            tz[k].y = ans_spline(ty, y);
        }
    }
    if (s3 < size) {
        ans = ans_newton(tz, z, s3);
    } else {
        ans = ans_spline(tz, z);
    }
    std::cout << "Ответ: " << ans << '\n';
}

double ans_newton(std::vector<table_line_t> &table, const double x, size_t n) {
    if (n + 1 > table.size())
        throw "Interpolation error";
    std::vector<double> x_table(n + 1, 0);
    std::vector<std::vector<double> > y_table(n + 1);
    table_line_t tmp{x, 0};
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
    for (size_t i = 0; i < n + 1; ++i) {
        //std::cout << ans << ' ' << xp << '\n';
        ans += y_table[0][i] * xp;
        //std::cout << "X: " << x << ' ' << x_table[i] << '\n';
        xp *= x - x_table[i];
    }
    //std::cout << ans << ' ' << xp << '\n';
    return ans;
}

double ans_spline(std::vector<table_line_t> &table, const double x, const double c0, const double cn) {
    std::vector<double> a, b, c, d, k, t, h;

    for (size_t i = 1; i < table.size(); ++i) {
        a.push_back(table[i - 1].y);
        h.push_back(table[i].x - table[i - 1].x);
    }

    c.assign(table.size() - 1, 0);
    k.assign(table.size(), 0);
    t.assign(table.size(), 0);
    c[0] = cn;
    c[1] = c0;
    k[1] = t[1] = c0 / 2;

    for (size_t i = 2; i < table.size(); ++i) {
        double f = 3 * (((table[i].y - table[i - 1].y) / h[i - 1]) - ((table[i - 1].y - table[i - 2].y) / h[i - 2]));
        k[i] = -1 * h[i - 1] / (2 * (h[i - 1] + h[i - 2]) + h[i - 2] * k[i - 1]);
        t[i] = (f - h[i - 2] * t[i - 1]) / (2 * (h[i - 1] + h[i - 2]) + h[i - 2] * k[i - 1]);
    }

    c.back() = k.back() * cn + t.back();

    for (size_t i = table.size() - 2; i; --i) {
        c[i - 1] = c[i] * k[i] + t[i];
    }

    for (size_t i = 0; i < c.size() - 1; ++i) {
        b.push_back((a[i + 1] - a[i]) / h[i] - (h[i] * (2 * c[i + 1] + c[i])) / 3);
        d.push_back((c[i + 1] - c[i]) / (3 * h[i]));
    }

    b.push_back((table.back().y - a.back()) / h.back() - (h.back() * (2 * cn + c.back())) / 3);
    d.push_back((cn - c.back()) / (3 * h.back()));

    size_t pos = 1;
    for (; pos < table.size() && x >= table[pos].x; ++pos);
    --pos;
    if (pos == table.size() - 1) {
        return table.back().y;
    }
    return a[pos] + b[pos] * (x - table[pos].x) + c[pos] * pow(x - table[pos].x, 2) + d[pos] * pow(x - table[pos].x, 3);
}
