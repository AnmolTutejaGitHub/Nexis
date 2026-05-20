package MyApp::Utils;

use strict;
use warnings;
use JSON;
use POSIX qw(floor ceil);

sub new {
    my ($class, %args) = @_;
    my $self = {
        config => $args{config} // {},
        cache  => {},
    };
    return bless $self, $class;
}

sub parse_config {
    my ($self, $file) = @_;
    open(my $fh, '<', $file) or die "Cannot open $file: $!";
    local $/;
    my $content = <$fh>;
    close $fh;
    return decode_json($content);
}

sub validate_data {
    my ($data) = @_;
    return defined $data && ref $data eq 'HASH' && scalar keys %$data > 0;
}

sub format_output {
    my ($data, $pretty) = @_;
    return $pretty ? to_json($data, { pretty => 1 }) : to_json($data);
}

1;
