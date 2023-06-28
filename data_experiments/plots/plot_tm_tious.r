library(ggplot2)

# List the filenames of the CSV files
csv_files <- c("mAP_results_tIoU_0.3.csv", "mAP_results_tIoU_0.4.csv", "mAP_results_tIoU_0.5.csv", "mAP_results_tIoU_0.6.csv", "mAP_results_tIoU_0.7.csv")

# Define the colors for each line
line_colors <- c("red", "blue", "green", "purple", "orange")

# Read and combine the data from all CSV files
data <- lapply(csv_files, function(file) {
  df <- read.csv(file, stringsAsFactors = FALSE)
  df$tIoU <- as.numeric(gsub("mAP_results_tIoU_", "", gsub(".csv", "", file)))
  df
})
combined_data <- do.call(rbind, data)

# Convert Percentage column to numeric
combined_data$Percentage <- as.numeric(combined_data$Percentage)

# Plot the graph with adjusted x-axis distances
plot <- ggplot(combined_data, aes(x = Percentage, y = `Average.mAP`, group = tIoU)) +
  geom_line(aes(color = factor(tIoU)), linetype = "solid", size = 1.2) +
  geom_point(shape = 19, size = 3) +
  scale_color_manual(values = line_colors) +
  labs(x = "Percentage", y = "mAP", color = "tIoU") +
  scale_x_continuous(breaks = c(0.1, 0.2, 0.4, 0.6, 0.8, 1.0), labels = c("0.1", "0.2", "0.4", "0.6", "0.8", "1.0")) +
  theme_bw()

ggsave("learning_curve_plot.png", plot, width = 8, height = 6, dpi = 300)
