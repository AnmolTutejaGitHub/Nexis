#include <string>
#include <vector>

class Database {
private:
    std::string connection_string;

public:
    Database(std::string conn);
    bool connect();
    void disconnect();
    std::vector<std::string> query(std::string sql);
};

int calculate_checksum(const std::string& data) {
    return data.size();
}

bool validate_input(const std::string& input) {
    return !input.empty();
}
