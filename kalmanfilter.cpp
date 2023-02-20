#include <Eigen/Dense> // Eigen is a C++ library for matrix operations

class KalmanFilter {
public:
    // Constructor
    KalmanFilter(int n, int m, int p) : n(n), m(m), p(p) {
        x = Eigen::VectorXd::Zero(n); // Initialize state vector x
        P = Eigen::MatrixXd::Identity(n, n); // Initialize state covariance matrix P
        F = Eigen::MatrixXd::Identity(n, n); // Initialize state transition matrix F
        H = Eigen::MatrixXd::Zero(m, n); // Initialize observation matrix H
        Q = Eigen::MatrixXd::Identity(n, n); // Initialize process noise covariance matrix Q
        R = Eigen::MatrixXd::Identity(m, m); // Initialize observation noise covariance matrix R
    }
    
    // Prediction Step
    void predict() {
        x = F * x;
        P = F * P * F.transpose() + Q;
    }
    
    // Update Step
    void update(const Eigen::VectorXd& z) {
        Eigen::VectorXd y = z - H * x;
        Eigen::MatrixXd S = H * P * H.transpose() + R;
        Eigen::MatrixXd K = P * H.transpose() * S.inverse();
        x = x + K * y;
        P = (Eigen::MatrixXd::Identity(n, n) - K * H) * P;
    }
    
    // Setters
    void setState(const Eigen::VectorXd& x) { this->x = x; }
    void setCovariance(const Eigen::MatrixXd& P) { this->P = P; }
    void setTransition(const Eigen::MatrixXd& F) { this->F = F; }
    void setObservation(const Eigen::MatrixXd& H) { this->H = H; }
    void setProcessNoise(const Eigen::MatrixXd& Q) { this->Q = Q; }
    void setObservationNoise(const Eigen::MatrixXd& R) { this->R = R; }
    
    // Getters
    Eigen::VectorXd getState() const { return x; }
    Eigen::MatrixXd getCovariance() const { return P; }
    Eigen::MatrixXd getTransition() const { return F; }
    Eigen::MatrixXd getObservation() const { return H; }
    Eigen::MatrixXd getProcessNoise() const { return Q; }
    Eigen::MatrixXd getObservationNoise() const { return R; }
    
private:
    int n; // State dimension
    int m; // Observation dimension
    int p; // Control dimension
    Eigen::VectorXd x; // State vector
    Eigen::MatrixXd P; // State covariance matrix
    Eigen::MatrixXd F; // State transition matrix
    Eigen::MatrixXd H; // Observation matrix
    Eigen::MatrixXd Q; // Process noise covariance matrix
    Eigen::MatrixXd R; // Observation noise covariance matrix
};
