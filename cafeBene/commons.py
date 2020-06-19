from flask import Flask, Blueprint, request, render_template, flash, redirect, url_for
import json
import pandas as pd
import numpy as np
import pymysql
from datetime import datetime, date
import threading
import schedule
import time
import requests


DEPOSIT = 500