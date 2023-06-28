# Load the required libraries
library(ggplot2)

# Read the data from the CSV files
temporalmaxer <- read.csv("temporalmaxer.csv")
actionformer <- read.csv("actionformer.csv")
tridet <- read.csv("tridet.csv")
tadtr <- read.csv("tadtr.csv")

# Convert percentage column to numeric
temporalmaxer$percentage <- as.numeric(gsub("%", "", temporalmaxer$percentage))
actionformer$percentage <- as.numeric(gsub("%", "", actionformer$percentage))
tridet$percentage <- as.numeric(gsub("%", "", tridet$percentage))
tadtr$percentage <- as.numeric(gsub("%", "", tadtr$percentage))

# Define the colors for each model
model_colors <- c("ActionFormer" = "blue", "TriDet" = "red", "TadTR" = "green", "TemporalMaxer" = "orange")

# Plot for TemporalMaxer
plot_temporalmaxer <- ggplot(data = temporalmaxer, aes(x = percentage, y = mAP)) + 
  geom_line(size = 1) +
  geom_ribbon(aes(ymin = mAP - std, ymax = mAP + std), fill = "steelblue3", alpha = 0.3) +
  labs(x = "Percentage of Dataset Utilized", y = "mAP") +
  ggtitle("TemporalMaxer") +
  theme_bw() +
  theme(legend.position = "none")  # Remove the legend

# Plot for all 4 models
plot_comparison <- ggplot() +
  geom_line(data = actionformer, aes(x = percentage, y = mAP, color = "ActionFormer"), size = 1) +
  geom_ribbon(data = actionformer, aes(x = percentage, ymin = mAP - std, ymax = mAP + std), fill = "steelblue3", alpha = 0.3) +
  geom_line(data = tridet, aes(x = percentage, y = mAP, color = "TriDet"), size = 1) +
  geom_ribbon(data = tridet, aes(x = percentage, ymin = mAP - std, ymax = mAP + std), fill = "red", alpha = 0.3) +
  geom_line(data = tadtr, aes(x = percentage, y = mAP, color = "TadTR"), size = 1) +
  geom_ribbon(data = tadtr, aes(x = percentage, ymin = mAP - std, ymax = mAP + std), fill = "green", alpha = 0.3) +
  geom_line(data = temporalmaxer, aes(x = percentage, y = mAP, color = "TemporalMaxer"), size = 1) +
  geom_ribbon(data = temporalmaxer, aes(x = percentage, ymin = mAP - std, ymax = mAP + std), fill = "orange", alpha = 0.3) +
  labs(x = "Percentage of Dataset Utilized", y = "mAP") +
  ggtitle("Comparison of Models") +
  theme_bw() +
  theme(legend.position = "none")  # Remove the legend

# Combine the plots and add the legend
combined_plot <- plot_comparison +
  scale_color_manual(values = model_colors) +
  guides(color = guide_legend(title = "Models"))  # Add the legend

# Save the plots as images
ggsave("plot_temporalmaxer.png", plot = plot_temporalmaxer, width = 8, height = 6)
ggsave("plot_comparison.png", plot = combined_plot, width = 8, height = 6)

# View the plots
plot_temporalmaxer
combined_plot
