#!/usr/bin/perl

use strict;
use warnings;
use IO::Socket::INET;
use JSON;

my $host = 'localhost';
my $port = 8080;
my $socket = new IO::Socket::INET (
    PeerHost => $host,
    PeerPort => $port,
    Proto => 'tcp',
);

die "Could not connect to $host:$port: $!\n" unless $socket;

print "Connected to $host:$port\n";

while (1) {
    my $json_data = <$socket>;
    last unless defined $json_data;

    my $json = decode_json($json_data);
    my $number = $json->{number};

    print "Received random number: $number\n";
}

close $socket;
print "Disconnected from $host:$port\n";