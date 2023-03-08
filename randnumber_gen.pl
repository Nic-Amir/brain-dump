#!/usr/bin/perl

use strict;
use warnings;
use Net::WebSocket::Server;
use JSON;

my $port = 8080;
my $server = Net::WebSocket::Server->new(
    listen => $port,
    on_connect => sub {
        my ($serv, $conn) = @_;
        print "Client connected from ", $conn->ip, "\n";

        $conn->on(
            utf8 => sub {
                my ($conn, $msg) = @_;
                my $json = JSON->new->decode($msg);
                print "Received message: ", $json->{message}, "\n";
            }
        );

        $conn->on(
            disconnect => sub {
                print "Client disconnected\n";
            }
        );
    }
);

$server->start;
