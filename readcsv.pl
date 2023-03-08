#!/usr/bin/perl

use strict;
use warnings;
use Text::CSV;

# Open the CSV file
my $csv = Text::CSV->new({ binary => 1 }) or die "Cannot use CSV: " . Text::CSV->error_diag();
open my $fh, "<", "data.csv" or die "data.csv: $!";

# Read the data and calculate the mean and standard deviation
my @data;
my $sum = 0;

while (my $row = $csv->getline($fh)) {
    push @data, @$row;
    $sum += $_ for @$row;
}

my $mean = $sum / scalar(@data);
my $sqsum = 0;
$sqsum += ($_ - $mean)**2 for @data;
my $stdev = sqrt($sqsum / (scalar(@data) - 1));

# Round the mean and standard deviation to two decimal places
$mean = sprintf("%.2f", $mean);
$stdev = sprintf("%.2f", $stdev);

# Print the mean and standard deviation
#print "Mean: $mean\n";
#print "Standard deviation: $stdev\n";

# Write the mean and standard deviation to the output file
open my $output_fh, ">", "output.txt" or die "output.txt: $!";
print $output_fh "Mean: $mean\n";
print $output_fh "Standard deviation: $stdev\n";
close $output_fh;


