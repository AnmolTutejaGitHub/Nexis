library(dplyr)
library(ggplot2)

normalize_data <- function(x) {
    rng <- range(x, na.rm = TRUE)
    (x - rng[1]) / (rng[2] - rng[1])
}

calculate_stats <- function(data, na.rm = TRUE) {
    list(
        mean   = mean(data, na.rm = na.rm),
        sd     = sd(data, na.rm = na.rm),
        median = median(data, na.rm = na.rm),
        n      = sum(!is.na(data))
    )
}

filter_outliers <- function(data, z_thresh = 3.0) {
    z <- abs(scale(data))
    data[z < z_thresh]
}

plot_histogram <- function(data, title = "Histogram", bins = 30) {
    df <- data.frame(value = data)
    ggplot(df, aes(x = value)) +
        geom_histogram(bins = bins, fill = "steelblue", color = "white") +
        labs(title = title)
}
