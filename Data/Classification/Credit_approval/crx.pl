#!/usr/bin/perl
sub getind($%);
sub getval($\@\%);
sub mkindex(@);
sub putval($$\@\%);
sub readlist($);
sub readln($);
sub writelist($@);
sub writeln($$);

$DLM = ",";
$INFILE = "crx.data";
$OUTFILE = "crx.csv";
$NVAR = 15;

open STDIN, "<", $INFILE || die "Failure to open input file $INFILE: $!\n";
open STDOUT, ">", $OUTFILE || die "Failure to open output file $OUTFILE: $!\n";

@names = ();
for (my $i = 1; $i <= $NVAR; $i++) {push @names, "A".$i}
push @names, "class";
%index = &mkindex(@names);

&writelist(STDOUT, @names);
while (!eof(STDIN)) {
  my @values = &readlist(STDIN);
  my $class0 = &getval("class", \@values, \%index);
  my $class;
  if ($class0 eq "+") {$class = 1}
  elsif ($class0 eq "-") {$class = 0}
  for (my $i = 0; $i < $NVAR; $i++) {
    if ($values[$i]  eq "?") {$values[$i] = ""}
  }
  &putval("class", $class, \@values, \%index);
  &writelist(STDOUT, @values);
}

sub getind($%) {
  my ($name, %index) = @_;
  my $index = $index{$name};
  if (!defined($index)) {die}
  return $index;
}

sub getval($\@\%) {
  my ($name, $pbuf, $pindex) = @_;
  my $index = &getind($name, %$pindex);
  return $$pbuf[$index];
}

sub mkindex(@) {
  my $nvar = @name = @_;
  my %index;
  for (my $i = 0; $i < $nvar; $i++) {$index{$name[$i]} = $i}
  return %index;
}

sub putval($$\@\%) {
  my ($name, $value, $pbuf, $pindex) = @_;
  my $index = &getind($name, %index);
  $$pbuf[$index] = $value;
}

sub readlist($) {
  my ($fh) = @_;
  my $line = &readln($fh);
  return split($DLM, $line);
}

sub readln($) {
  my ($fh) = @_;
  my $line = <$fh>;
  chomp $line;
  return $line;
}

sub writelist($@) {
  my ($fh, @list) = @_;
  &writeln($fh, join($DLM, @list));
}

sub writeln($$) {
  my ($fh, $line) = @_;
  print $fh "$line\n";
}
